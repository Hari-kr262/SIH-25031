"""Dashboard routes: public stats, admin stats, department stats."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.user import User, UserRole
from backend.services.analytics_service import analytics_service
from backend.middleware.rbac_middleware import require_admin, require_department_head
from backend.utils.response_utils import success_response

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/public", response_model=dict)
def public_dashboard(db: Session = Depends(get_db)):
    """Public stats visible to anyone."""
    stats = analytics_service.get_overview_stats(db)
    stats["issues_by_category"] = analytics_service.get_issues_by_category(db)
    stats["issues_by_status"] = analytics_service.get_issues_by_status(db)
    stats["top_wards"] = analytics_service.get_top_wards(db)
    return success_response(stats)


@router.get("/admin", response_model=dict)
def admin_dashboard(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Admin-level stats including user counts and SLA metrics."""
    from backend.models.user import User as UserModel
    from backend.services.sla_service import sla_service

    stats = analytics_service.get_overview_stats(db)
    stats["issues_by_category"] = analytics_service.get_issues_by_category(db)
    stats["issues_by_status"] = analytics_service.get_issues_by_status(db)
    stats["top_wards"] = analytics_service.get_top_wards(db)
    stats["total_users"] = db.query(UserModel).count()
    stats["active_citizens"] = db.query(UserModel).filter_by(role=UserRole.citizen, is_active=True).count()
    stats["total_volunteers"] = db.query(UserModel).filter_by(role=UserRole.volunteer, is_active=True).count()
    stats["total_workers"] = db.query(UserModel).filter_by(role=UserRole.field_worker, is_active=True).count()
    breached = sla_service.get_breached_issues(db)
    at_risk = sla_service.get_at_risk_issues(db)
    stats["sla_breached"] = len(breached)
    stats["sla_at_risk"] = len(at_risk)
    stats["department_performance"] = analytics_service.get_department_performance(db)
    return success_response(stats)


@router.get("/department", response_model=dict)
def department_dashboard(
    current_user: User = Depends(require_department_head),
    db: Session = Depends(get_db),
):
    """Department-specific stats for department heads."""
    from backend.models.issue import Issue, IssueStatus

    dept_id = current_user.department_id
    if not dept_id:
        return success_response({})
    total = db.query(Issue).filter_by(department_id=dept_id).count()
    resolved = db.query(Issue).filter_by(department_id=dept_id, status=IssueStatus.resolved).count()
    pending = db.query(Issue).filter_by(department_id=dept_id, status=IssueStatus.pending).count()
    in_progress = db.query(Issue).filter_by(department_id=dept_id, status=IssueStatus.in_progress).count()

    return success_response({
        "total_issues": total,
        "resolved": resolved,
        "pending": pending,
        "in_progress": in_progress,
        "resolution_rate": round(resolved / total * 100, 2) if total > 0 else 0,
    })
