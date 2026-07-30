"""
Sentinel — Ticket View Interface
UI components for ticket management, sentiment view, and resolution recommendations.
"""
from __future__ import annotations

from typing import Any, Dict, List
import streamlit as st

from rag.rag_engine import RAGEngine
from nlp.sentiment_analyzer import SentimentAnalyzer
from nlp.ticket_classifier import TicketClassifier


def render_ticket_interface(
    rag_engine: RAGEngine,
    classifier: TicketClassifier,
    analyzer: SentimentAnalyzer,
    query_history: List[Dict[str, Any]],
) -> None:
    """Render support ticket ingestion and response generation tab."""
    st.subheader("🎫 Process Customer Ticket")

    ticket_text = st.text_area(
        "Enter support ticket description",
        placeholder="Type customer complaint or support request here...",
        height=150,
    )

    col1, col2 = st.columns(2)
    with col1:
        process_btn = st.button(
            "🛡️ Process Ticket",
            type="primary",
            use_container_width=True,
            disabled=len(ticket_text.strip()) == 0,
        )
    with col2:
        clear_btn = st.button("🗑️ Reset", use_container_width=True)

    if clear_btn:
        st.session_state.query_history = []
        st.rerun()

    if process_btn and ticket_text.strip():
        with st.spinner("🔍 Running classification and sentiment analysis..."):
            # Classify
            class_res = classifier.classify(ticket_text)
            category = class_res["category"]
            priority = class_res["priority"]

            # Sentiment
            sentiment_res = analyzer.analyze(ticket_text)
            sentiment = sentiment_res["sentiment"]
            sentiment_score = sentiment_res["score"]

            # Retrieve context
            context = rag_engine.retrieve_context(ticket_text)

            # Generate Response
            response_text = rag_engine.generate_response(
                query=ticket_text,
                context=context,
                sentiment=sentiment,
                priority=priority,
            )

            # Append to session state
            st.session_state.query_history.append({
                "ticket": ticket_text,
                "category": category,
                "priority": priority,
                "sentiment": sentiment,
                "sentiment_score": sentiment_score,
                "response": response_text,
                "context": context,
            })

    # Render results from history
    if query_history:
        latest = query_history[-1]

        st.divider()
        st.subheader("✨ Sentinel Support Recommendations")

        col_meta1, col_meta2, col_meta3 = st.columns(3)
        with col_meta1:
            st.markdown(f"📁 **Category:** `{latest['category']}`")
        with col_meta2:
            st.markdown(f"🚨 **Urgency:** `{latest['priority']}`")
        with col_meta3:
            st.markdown(f"🎭 **Sentiment:** `{latest['sentiment']}` (Score: `{latest['sentiment_score']:.2f}`)")

        st.subheader("✍️ Suggested Support Response")
        st.info(latest["response"])

        with st.expander("📚 Reference Context Used"):
            if latest["context"]:
                for idx, doc in enumerate(latest["context"], 1):
                    st.markdown(f"**Source Context {idx} (Relevance Score: {doc['similarity']:.2%})**")
                    st.write(doc["content"])
                    st.divider()
            else:
                st.write("No matching historical resolutions found in FAISS database.")
