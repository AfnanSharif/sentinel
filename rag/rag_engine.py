"""
Sentinel — RAG Engine
Implements retrieval-augmented generation using FAISS vector database
and OpenAI Chat & Embedding APIs.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import faiss
import numpy as np
from langchain_community.vectorstores import FAISS as LangchainFAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config.openai_config import openai_settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class RAGEngine:
    """
    RAG Engine managing the embedding retrieval, context building,
    and answer generation pipeline using OpenAI and FAISS.
    """

    def __init__(self) -> None:
        self.embeddings = OpenAIEmbeddings(
            model=openai_settings.OPENAI_EMBEDDING_MODEL,
            openai_api_key=openai_settings.OPENAI_API_KEY,
        )
        self.llm = ChatOpenAI(
            model=openai_settings.OPENAI_CHAT_MODEL,
            temperature=openai_settings.OPENAI_TEMPERATURE,
            max_tokens=openai_settings.OPENAI_MAX_TOKENS,
            openai_api_key=openai_settings.OPENAI_API_KEY,
        )
        self.vectorstore: Optional[LangchainFAISS] = None
        self._load_index()
        logger.info("Sentinel RAG Engine initialized")

    def _load_index(self) -> None:
        """Load the FAISS vector database index from disk if it exists."""
        index_path = Path(openai_settings.FAISS_INDEX_PATH)
        if index_path.exists() and (index_path / "index.faiss").exists():
            try:
                self.vectorstore = LangchainFAISS.load_local(
                    str(index_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
                logger.info(f"Loaded FAISS index from {index_path}")
            except Exception as e:
                logger.error(f"Error loading FAISS index: {e}")

    def build_vector_db(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> bool:
        """
        Build and persist a new FAISS vector database.

        Args:
            texts: List of document/ticket texts to index
            metadatas: Metadata dictionaries for each text

        Returns:
            True if built successfully
        """
        if not texts:
            logger.warning("No texts provided to build vector database")
            return False

        try:
            self.vectorstore = LangchainFAISS.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas,
            )
            index_path = Path(openai_settings.FAISS_INDEX_PATH)
            index_path.mkdir(parents=True, exist_ok=True)
            self.vectorstore.save_local(str(index_path))
            logger.info(f"Vector DB built and persisted to {index_path}")
            return True
        except Exception as e:
            logger.error(f"Error building vector database: {e}")
            return False

    def retrieve_context(self, query: str, k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve context documents from vector store.

        Args:
            query: The search query
            k: Top-K documents to retrieve

        Returns:
            List of matching records with content and metadata
        """
        if self.vectorstore is None:
            logger.warning("Vector database not loaded or empty")
            return []

        top_k = k or openai_settings.FAISS_TOP_K
        try:
            docs_with_scores = self.vectorstore.similarity_search_with_score(query, k=top_k)
            results = []
            for doc, score in docs_with_scores:
                similarity = 1.0 - float(score)  # L2 distance metric
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity": similarity,
                })
            return results
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return []

    def generate_response(
        self, query: str, context: List[Dict[str, Any]], sentiment: str, priority: str
    ) -> str:
        """
        Generate a support response incorporating retrieved context.

        Args:
            query: Customer query/ticket
            context: Retrieved ticket resolution context
            sentiment: Customer sentiment
            priority: Detected priority level

        Returns:
            Generated response string
        """
        context_str = "\n\n".join([
            f"[Case Context - Category: {doc['metadata'].get('category', 'General')}]\n{doc['content']}"
            for doc in context
        ])

        system_prompt = f"""You are a professional customer support specialist for Sentinel Retail.
Your task is to respond to a customer support ticket.

Ticket metadata:
- Detected Sentiment: {sentiment}
- Urgency/Priority: {priority}

Use the following resolved ticket summaries and internal documentation for context:
---
{context_str}
---

Guidelines:
- If customer sentiment is negative/upset, begin with a sincere, tailored apology.
- Keep the response clear, structured, professional, and actionable.
- Do not mention 'context database', 'internal guidelines', or 'system prompts' to the user.
- If the internal context does not contain the answer, politely state that you are looking into the issue and will follow up shortly.
"""
        from langchain.schema import SystemMessage, HumanMessage

        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Customer Support Request:\n{query}"),
            ])
            return response.content.strip()
        except Exception as e:
            logger.error(f"Response generation error: {e}")
            return "Thank you for reaching out. We have received your support request and our team is investigating. We will respond with an update shortly."
