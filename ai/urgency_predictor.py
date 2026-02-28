"""
Urgency predictor — estimates urgency score (0-1) for civic issues.
Uses category, keywords, and historical patterns.
"""



URGENCY_WEIGHTS = {
    "water_leak": 0.9,
    "sewage": 0.85,
    "fallen_tree": 0.85,
    "pothole": 0.7,
    "drainage": 0.65,
    "road_damage": 0.6,
    "garbage": 0.5,
    "illegal_dumping": 0.55,
    "streetlight": 0.5,
    "public_property": 0.4,
    "other": 0.5,
}

URGENCY_KEYWORDS = {
    "high": ["burst", "flooding", "accident", "blocked road", "main road", "emergency",
             "hospital", "school", "critical", "danger", "unsafe"],
    "low": ["minor", "small", "slight", "cosmetic"],
}


class UrgencyPredictor:
    """Predicts urgency score for a civic issue."""

    def predict(
        self,
        category: str,
        description: str = "",
        upvotes: int = 0,
    ) -> float:
        """
        Return urgency score between 0 and 1.
        Higher = more urgent.
        """
        base_score = URGENCY_WEIGHTS.get(category, 0.5)

        # Keyword adjustment
        text_lower = description.lower()
        keyword_boost = 0.0
        for kw in URGENCY_KEYWORDS["high"]:
            if kw in text_lower:
                keyword_boost += 0.05
        for kw in URGENCY_KEYWORDS["low"]:
            if kw in text_lower:
                keyword_boost -= 0.05

        # Vote-based adjustment (more votes = more urgent)
        vote_boost = min(0.1, upvotes * 0.01)

        score = base_score + keyword_boost + vote_boost
        return round(min(1.0, max(0.0, score)), 3)


urgency_predictor = UrgencyPredictor()
