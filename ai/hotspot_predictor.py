"""
Hotspot predictor — identifies geographic clusters of civic issues.
Uses K-means clustering to find problem hotspots.
"""

from typing import List, Dict, Optional
import math


class HotspotPredictor:
    """Identifies civic issue hotspots using clustering."""

    def predict_hotspots(
        self,
        issues: List[Dict],
        n_clusters: int = 5,
        min_cluster_size: int = 3,
    ) -> List[Dict]:
        """
        Find geographic hotspots from issue data.
        Returns list of hotspot center points with issue counts.
        """
        # Filter issues with coordinates
        geo_issues = [i for i in issues if i.get("latitude") and i.get("longitude")]
        if len(geo_issues) < min_cluster_size:
            return []

        try:
            import numpy as np
            from sklearn.cluster import KMeans

            coords = np.array([[i["latitude"], i["longitude"]] for i in geo_issues])
            n = min(n_clusters, len(geo_issues))
            kmeans = KMeans(n_clusters=n, random_state=42, n_init="auto")
            labels = kmeans.fit_predict(coords)

            hotspots = []
            for cluster_id in range(n):
                cluster_issues = [geo_issues[i] for i, l in enumerate(labels) if l == cluster_id]
                if len(cluster_issues) >= min_cluster_size:
                    center = kmeans.cluster_centers_[cluster_id]
                    hotspots.append({
                        "lat": float(center[0]),
                        "lng": float(center[1]),
                        "issue_count": len(cluster_issues),
                        "categories": list({i.get("category") for i in cluster_issues}),
                        "severity": "high" if len(cluster_issues) > 10 else "medium" if len(cluster_issues) > 5 else "low",
                    })
            return sorted(hotspots, key=lambda x: x["issue_count"], reverse=True)

        except ImportError:
            return self._simple_grid_hotspots(geo_issues)

    def _simple_grid_hotspots(self, issues: List[Dict]) -> List[Dict]:
        """Grid-based hotspot detection fallback."""
        from collections import defaultdict
        grid = defaultdict(list)
        for issue in issues:
            key = (round(issue["latitude"], 2), round(issue["longitude"], 2))
            grid[key].append(issue)

        hotspots = []
        for (lat, lng), cluster_issues in grid.items():
            if len(cluster_issues) >= 2:
                hotspots.append({
                    "lat": lat,
                    "lng": lng,
                    "issue_count": len(cluster_issues),
                    "severity": "high" if len(cluster_issues) > 5 else "medium",
                })
        return sorted(hotspots, key=lambda x: x["issue_count"], reverse=True)


hotspot_predictor = HotspotPredictor()
