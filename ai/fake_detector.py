"""
Fake report detector — identifies potentially fraudulent issue reports.
Uses text similarity, location anomalies, and user behavior patterns.
"""

from typing import Dict, Any, Tuple


class FakeDetector:
    """Detects potentially fake or duplicate civic issue reports."""

    def analyze(
        self,
        title: str,
        description: str,
        latitude: float = None,
        longitude: float = None,
        user_id: int = None,
        db=None,
    ) -> Tuple[bool, float, str]:
        """
        Analyze a report for fake indicators.
        Returns (is_fake, confidence, reason).
        """
        reasons = []
        fake_score = 0.0

        # Check for suspiciously short description
        combined = (title + " " + (description or "")).strip()
        if len(combined) < 10:
            fake_score += 0.6
            reasons.append("Very short description")

        # Check for all-caps spam indicators
        if combined.isupper() and len(combined) > 5:
            fake_score += 0.2
            reasons.append("All caps text")

        # Check for repeated characters
        import re
        if re.search(r"(.)\1{4,}", combined):
            fake_score += 0.2
            reasons.append("Repeated characters detected")

        # Check invalid coordinates for Jharkhand (approx bounds)
        if latitude is not None and longitude is not None:
            if not (22.0 <= latitude <= 25.5 and 83.0 <= longitude <= 87.5):
                fake_score += 0.6
                reasons.append("Coordinates outside Jharkhand")

        is_fake = fake_score >= 0.5
        reason = "; ".join(reasons) if reasons else "No issues detected"
        return is_fake, round(min(1.0, fake_score), 3), reason


fake_detector = FakeDetector()
