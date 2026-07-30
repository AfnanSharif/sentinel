"""
Sentinel — Vector Database Builder
Creates mock resolution guides and indexes them into FAISS using OpenAI Embeddings.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add root folder
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.rag_engine import RAGEngine


def main() -> None:
    """Generates mock data and indexes it into FAISS."""
    print("🛡️ Building Sentinel Vector Database...")

    # Define some customer support resolution guides
    guides = [
        "To process a billing refund, verify the transaction ID in stripe. Credit takes 3-5 business days.",
        "If a customer's package is marked delivered but not received, check tracking updates and contact FedEx support.",
        "To reset passwords, user must use the 'Forgot Password' link from the login page. Admin resets are disallowed for security.",
        "Quality issues require the customer to upload a photo of the damaged product before we dispatch a replacement.",
    ]

    metadatas = [
        {"category": "Billing & Payments", "source": "billing_guide.txt"},
        {"category": "Shipping & Logistics", "source": "shipping_guide.txt"},
        {"category": "Technical Support", "source": "tech_guide.txt"},
        {"category": "Product Inquiry & Quality", "source": "product_guide.txt"},
    ]

    try:
        engine = RAGEngine()
        success = engine.build_vector_db(guides, metadatas)
        if success:
            print("✅ Sentinel FAISS Vector DB built successfully!")
        else:
            print("❌ Failed to build Sentinel Vector DB.")
    except Exception as e:
        print(f"❌ Error during Sentinel DB build: {e}")
        print("💡 Make sure you configured your OPENAI_API_KEY inside sentinel/.env")


if __name__ == "__main__":
    main()
