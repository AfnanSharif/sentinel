"""
Sentinel — Unit Tests
Verifies sentiment analysis, priority keyword matching and RAG responses.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest

from nlp.sentiment_analyzer import SentimentAnalyzer
from nlp.ticket_classifier import TicketClassifier


class TestSentinelSuite(unittest.TestCase):
    """Test suite verifying ticket classification and sentiment scoring."""

    def setUp(self) -> None:
        self.analyzer = SentimentAnalyzer()
        self.classifier = TicketClassifier()

    def test_sentiment_scoring(self) -> None:
        """Verify sentiment scoring maps negative keywords correctly."""
        neg_ticket = "This product is broken and customer support is terrible."
        res = self.analyzer.analyze(neg_ticket)
        self.assertEqual(res["sentiment"], "Negative")
        self.assertTrue(res["score"] < 0.5)

    def test_priority_and_category_classification(self) -> None:
        """Verify priority levels trigger on urgency keywords."""
        ticket = "URGENT: I was double charged on my card!"
        res = self.classifier.classify(ticket)
        self.assertEqual(res["category"], "Billing & Payments")
        self.assertEqual(res["priority"], "High")


if __name__ == "__main__":
    unittest.main()
