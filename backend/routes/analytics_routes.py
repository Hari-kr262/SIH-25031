"""Analytics routes: trends, heatmap, performance, SLA, export."""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.user import User
from backend.services.analytics_service import analytics_service
from backend.services.export_service import export_service
from backend.middleware.rbac_middleware import require_admin
from backend.utils.response_utils import success_response

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/trends", response_model=dict)
def issue_trends(
    days: int = Query(30, ge=7, le=365),
    db: Session = Depends(get_db),
):
    """Daily issue count trends."""
    data = analytics_service.get_trend_data(db, days=days)
    return success_response(data)


@router.get("/heatmap", response_model=dict)
def heatmap_data(db: Session = Depends(get_db)):
    """Geographic heatmap data — lat/lng points for all open issues."""
    from backend.models.issue import Issue, IssueStatus
    issues = db.query(Issue).filter(
        Issue.latitude.isnot(None),
        Issue.longitude.isnot(None),
        Issue.status.notin_([IssueStatus.closed, IssueStatus.rejected]),
    ).all()
    points = [{"lat": i.latitude, "lng": i.longitude, "weight": i.upvotes + 1} for i in issues]
    return success_response(points)


@router.get("/performance", response_model=dict)
def department_performance(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Department-wise resolution performance."""
    data = analytics_service.get_department_performance(db)
    return success_response(data)


@router.get("/sla", response_model=dict)
def sla_analytics(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """SLA compliance analytics."""
    from backend.services.sla_service import sla_service
    breached = sla_service.get_breached_issues(db)
    at_risk = sla_service.get_at_risk_issues(db)
    return success_response({
        "breached_count": len(breached),
        "at_risk_count": len(at_risk),
        "at_risk_issues": at_risk,
        "breached_issue_ids": [i.id for i in breached],
    })


@router.get("/export/pdf", response_class=Response)
def export_pdf(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Export analytics as PDF."""
    stats = analytics_service.get_overview_stats(db)
    pdf_bytes = export_service.generate_pdf_report({"stats": stats}, title="CivicResolve Analytics Report")
    return Response(content=pdf_bytes, media_type="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=civicresolve_report.pdf"})


@router.get("/export/excel", response_class=Response)
def export_excel(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Export issues as Excel."""
    from backend.models.issue import Issue
    issues = db.query(Issue).all()
    data = [{
        "id": i.id, "title": i.title, "category": i.category.value,
        "status": i.status.value, "priority": i.priority.value,
        "ward": i.ward, "created_at": str(i.created_at),
    } for i in issues]
    excel_bytes = export_service.generate_excel_report(data)
    return Response(content=excel_bytes,
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": "attachment; filename=issues.xlsx"})
