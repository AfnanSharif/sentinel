"""
Sentinel — Ticket Classifier
Classifies ticket content into predefined retail support categories.
"""
from __future__ import annotations

from typing import Dict

from utils.logger import setup_logger

logger = setup_logger(__name__)


class TicketClassifier:
    """
    Classifies customer support tickets into retail categories like
    Billing, Shipping, Technical, Product, or General Support.
    """

    def __init__(self) -> None:
        logger.info("Ticket Classifier initialized")

    def classify(self, text: str) -> Dict[str, str]:
        """
        Classify support request into a category and detect priority.

        Args:
            text: Customer support request text

        Returns:
            Dict containing 'category' and 'priority'
        """
        text_lower = text.lower()

        # Category detection
        category = "General Support"
        if any(w in text_lower for w in ["bill", "charge", "refund", "price", "payment", "invoice"]):
            category = "Billing & Payments"
        elif any(w in text_lower for w in ["ship", "track", "delivery", "order", "receive", "courier"]):
            category = "Shipping & Logistics"
        elif any(w in text_lower for w in ["login", "password", "bug", "app", "error", "website", "account"]):
            category = "Technical Support"
        elif any(w in text_lower for w in ["size", "color", "quality", "material", "warranty", "broken"]):
            category = "Product Inquiry & Quality"

        # Priority detection
        priority = "Medium"
        high_indicators = ["urgent", "asap", "broken", "critical", "charge double", "scam", "police", "legal"]
        low_indicators = ["just curious", "wondering", "future", "feedback", "idea"]

        if any(w in text_lower for w in high_indicators):
            priority = "High"
        elif any(w in text_lower for w in low_indicators):
            priority = "Low"

        return {
            "category": category,
            "priority": priority,
        }
