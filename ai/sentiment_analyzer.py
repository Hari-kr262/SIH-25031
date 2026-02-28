"""
Sentiment analyzer for citizen feedback and comments.
Uses VADER-like rules or sklearn for sentiment classification.
"""

from typing import Dict


class SentimentAnalyzer:
    """Analyzes sentiment of citizen feedback on resolved issues."""

    POSITIVE_WORDS = {
        "excellent", "great", "good", "amazing", "fantastic", "wonderful",
        "satisfied", "happy", "perfect", "awesome", "resolved", "fixed",
        "thank", "thanks", "appreciate", "helpful", "quick", "fast"
    }

    NEGATIVE_WORDS = {
        "bad", "terrible", "poor", "awful", "disappointed", "dissatisfied",
        "slow", "unresolved", "broken", "useless", "waste", "worst",
        "horrible", "unacceptable", "negligent", "ignore"
    }

    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment of text.
        Returns dict with sentiment (positive/negative/neutral) and score.
        """
        words = set(text.lower().split())
        pos_count = len(words & self.POSITIVE_WORDS)
        neg_count = len(words & self.NEGATIVE_WORDS)

        if pos_count > neg_count:
            sentiment = "positive"
            score = min(1.0, 0.5 + (pos_count - neg_count) * 0.1)
        elif neg_count > pos_count:
            sentiment = "negative"
            score = max(0.0, 0.5 - (neg_count - pos_count) * 0.1)
        else:
            sentiment = "neutral"
            score = 0.5

        return {
            "sentiment": sentiment,
            "score": round(score, 3),
            "positive_words": pos_count,
            "negative_words": neg_count,
        }


sentiment_analyzer = SentimentAnalyzer()
