"""Map routes: issues, heatmap, clusters, route."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.issue import Issue, IssueStatus
from backend.utils.response_utils import success_response

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
    Return approximate issue clusters.
    TODO: Implement K-means clustering using scikit-learn for production.
    """
    issues = db.query(Issue).filter(
        Issue.latitude.isnot(None),
        Issue.longitude.isnot(None),
        Issue.status.notin_([IssueStatus.closed, IssueStatus.rejected]),
    ).all()
    # Simple grouping by rounded coordinates as a stub
    from collections import defaultdict
    clusters_dict = defaultdict(list)
    for issue in issues:
        key = (round(issue.latitude, 2), round(issue.longitude, 2))
        clusters_dict[key].append(issue.id)

    return success_response([
        {"lat": k[0], "lng": k[1], "count": len(v), "issue_ids": v}
        for k, v in clusters_dict.items()
    ])
