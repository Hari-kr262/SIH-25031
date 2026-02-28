"""
Duplicate issue detector — finds similar existing reports.
Uses cosine similarity on TF-IDF vectors + Haversine distance.
"""

from typing import List, Dict, Any, Optional
import math


class DuplicateDetector:
    """Detects duplicate civic issue reports."""

    def find_duplicates(
        self,
        title: str,
        description: str,
        latitude: Optional[float],
        longitude: Optional[float],
        existing_issues: List[Dict[str, Any]],
        text_threshold: float = 0.7,
        geo_radius_km: float = 0.1,
    ) -> List[Dict[str, Any]]:
        """
        Find potential duplicates from a list of existing issues.
        Returns list of (issue, similarity_score) pairs.
        """
        candidates = []
        query_text = f"{title} {description or ''}".lower()

        for issue in existing_issues:
            score = 0.0
            issue_text = f"{issue.get('title', '')} {issue.get('description', '')}".lower()

            # Text similarity
            text_sim = self._simple_text_similarity(query_text, issue_text)
            score += text_sim * 0.6

            # Geographic proximity
            if latitude and longitude and issue.get("latitude") and issue.get("longitude"):
                dist = self._haversine(latitude, longitude, issue["latitude"], issue["longitude"])
                if dist <= geo_radius_km:
                    score += 0.4 * (1 - dist / geo_radius_km)

            if score >= text_threshold * 0.6:
                candidates.append({
                    "issue_id": issue.get("id"),
                    "title": issue.get("title"),
                    "similarity_score": round(score, 3),
                })

        return sorted(candidates, key=lambda x: x["similarity_score"], reverse=True)

    def _simple_text_similarity(self, text1: str, text2: str) -> float:
        """Jaccard similarity between word sets."""
        words1 = set(text1.split())
        words2 = set(text2.split())
        if not words1 or not words2:
            return 0.0
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union)

    def _haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Great-circle distance in km."""
        R = 6371
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return 2 * R * math.asin(math.sqrt(a))


duplicate_detector = DuplicateDetector()
