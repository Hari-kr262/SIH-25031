"""Map routes: issues, heatmap, clusters, route."""

import logging
import math
from collections import defaultdict

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.issue import Issue, IssueStatus
from backend.utils.response_utils import success_response

try:
    import numpy as np
    from sklearn.cluster import KMeans
    _sklearn_available = True
except ImportError:
    _sklearn_available = False

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/map", tags=["Map"])


@router.get("/issues", response_model=dict)
def map_issues(
    status: str = Query(None),
    category: str = Query(None),
    db: Session = Depends(get_db),
):
    """Get all georeferenced issues for map display."""
    query = db.query(Issue).filter(
        Issue.latitude.isnot(None),
        Issue.longitude.isnot(None),
    )
    if status:
        try:
            query = query.filter(Issue.status == IssueStatus(status))
        except ValueError:
            pass
    issues = query.all()
    return success_response([
        {
            "id": i.id,
            "title": i.title,
            "category": i.category.value,
            "status": i.status.value,
            "priority": i.priority.value,
            "lat": i.latitude,
            "lng": i.longitude,
            "address": i.address,
            "upvotes": i.upvotes,
        }
        for i in issues
    ])


@router.get("/heatmap", response_model=dict)
def heatmap(db: Session = Depends(get_db)):
    """Get heatmap data points (lat, lng, weight)."""
    issues = db.query(Issue).filter(
        Issue.latitude.isnot(None),
        Issue.longitude.isnot(None),
    ).all()
    return success_response([
        {"lat": i.latitude, "lng": i.longitude, "weight": i.upvotes + 1}
        for i in issues
    ])


@router.get("/clusters", response_model=dict)
def clusters(
    radius_km: float = Query(0.5),
    db: Session = Depends(get_db),
):
    """
    Return issue clusters using K-Means clustering (scikit-learn).
    Falls back to coordinate-rounding grouping if sklearn is unavailable or data is insufficient.
    """
    issues = db.query(Issue).filter(
        Issue.latitude.isnot(None),
        Issue.longitude.isnot(None),
        Issue.status.notin_([IssueStatus.closed, IssueStatus.rejected]),
    ).all()

    if not issues:
        return success_response([])

    coords = [(i.latitude, i.longitude) for i in issues]

    if _sklearn_available and len(coords) >= 2:
        try:
            n = len(coords)
            n_clusters = max(1, min(n, int(math.sqrt(n / 2)) or 1))

            X = np.array(coords)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
            labels = kmeans.fit_predict(X)

            clusters_dict: dict = defaultdict(list)
            for idx, label in enumerate(labels):
                clusters_dict[int(label)].append(issues[idx].id)

            centers = kmeans.cluster_centers_
            return success_response([
                {
                    "lat": round(float(centers[label][0]), 6),
                    "lng": round(float(centers[label][1]), 6),
                    "count": len(ids),
                    "issue_ids": ids,
                }
                for label, ids in clusters_dict.items()
            ])
        except Exception as exc:
            logger.warning("KMeans clustering failed, falling back to coordinate grouping: %s", exc)

    # Fallback: simple grouping by rounded coordinates
    fallback_dict: dict = defaultdict(list)
    for issue in issues:
        key = (round(issue.latitude, 2), round(issue.longitude, 2))
        fallback_dict[key].append(issue.id)

    return success_response([
        {"lat": k[0], "lng": k[1], "count": len(v), "issue_ids": v}
        for k, v in fallback_dict.items()
    ])
