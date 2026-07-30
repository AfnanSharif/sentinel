"""
Sentinel — Sentiment Analyzer
Provides sentiment scoring and categorisation for customer tickets.
"""
from __future__ import annotations

from utils.logger import setup_logger

logger = setup_logger(__name__)


class SentimentAnalyzer:
    """
    Analyzes raw customer text to extract sentiment scores and
    sentiment categories (Positive, Neutral, Negative).
    """

    def __init__(self) -> None:
        logger.info("Sentiment Analyzer initialized")

    def analyze(self, text: str) -> dict:
        """
        Analyze the sentiment of a support ticket.

        Args:
            text: Customer text query

        Returns:
            Dictionary containing sentiment analysis details
        """
        if not text or not text.strip():
            return {"sentiment": "Neutral", "score": 0.5, "magnitude": 0.0}

        # Rule-based fallback or lightweight scoring for offline support
        text_lower = text.lower()
        negative_words = {"angry", "upset", "unhappy", "terrible", "worst", "broken", "fail", "bad", "disappointed", "refund"}
        positive_words = {"happy", "thanks", "great", "excellent", "perfect", "good", "solved", "resolved", "love"}

        neg_count = sum(1 for word in negative_words if word in text_lower)
        pos_count = sum(1 for word in positive_words if word in text_lower)

        # Simple mapping to score (0 to 1)
        if neg_count > pos_count:
            sentiment = "Negative"
            score = max(0.1, 0.5 - (neg_count * 0.1))
        elif pos_count > neg_count:
            sentiment = "Positive"
            score = min(0.9, 0.5 + (pos_count * 0.1))
        else:
            sentiment = "Neutral"
            score = 0.5

        return {
            "sentiment": sentiment,
            "score": score,
            "magnitude": float(neg_count + pos_count),
        }
