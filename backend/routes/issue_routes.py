"""Issue routes: CRUD, my-issues, nearby, trending, assign, status, timeline."""

from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.issue import IssueStatus, IssueCategory, IssuePriority
from backend.models.user import User
from backend.schemas.issue import IssueCreate, IssueUpdate, IssueResponse, IssueAssign, IssueStatusUpdate
from backend.services.issue_service import issue_service
from backend.middleware.auth_middleware import get_current_user, get_optional_user
from backend.middleware.rbac_middleware import require_admin, require_department_head
from backend.utils.response_utils import success_response, paginated_response

router = APIRouter(prefix="/issues", tags=["Issues"])


@router.post("/", response_model=dict, status_code=201)
def create_issue(
    data: IssueCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Report a new civic issue."""
    issue = issue_service.create_issue(db, data, current_user.id)
    return success_response({"id": issue.id}, "Issue reported successfully")


@router.get("/", response_model=dict)
def list_issues(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[IssueStatus] = None,
    category: Optional[IssueCategory] = None,
    priority: Optional[IssuePriority] = None,
    department_id: Optional[int] = None,
    ward: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """List issues with optional filters."""
    items, total = issue_service.list_issues(
        db, page=page, page_size=page_size,
        status=status, category=category, priority=priority,
        department_id=department_id, ward=ward, search=search,
    )
    return paginated_response([IssueResponse.model_validate(i).model_dump() for i in items], total, page, page_size)


@router.get("/my", response_model=dict)
def my_issues(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get issues reported by the current user."""
    items, total = issue_service.list_issues(db, page=page, page_size=page_size, reporter_id=current_user.id)
    return paginated_response([IssueResponse.model_validate(i).model_dump() for i in items], total, page, page_size)


@router.get("/trending", response_model=dict)
def trending_issues(limit: int = Query(10, le=50), db: Session = Depends(get_db)):
    """Get trending issues ordered by upvotes."""
    issues = issue_service.get_trending(db, limit=limit)
    return success_response([IssueResponse.model_validate(i).model_dump() for i in issues])


@router.get("/nearby", response_model=dict)
def nearby_issues(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius_km: float = Query(2.0, le=50.0),
    db: Session = Depends(get_db),
):
    """Get issues near a location."""
    issues = issue_service.get_nearby(db, lat, lng, radius_km)
    return success_response([IssueResponse.model_validate(i).model_dump() for i in issues])


@router.get("/{issue_id}", response_model=IssueResponse)
def get_issue(issue_id: int, db: Session = Depends(get_db)):
    """Get a specific issue by ID."""
    return issue_service.get_issue(db, issue_id)


@router.put("/{issue_id}", response_model=IssueResponse)
def update_issue(
    issue_id: int,
    data: IssueUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an issue (author or admin only)."""
    issue = issue_service.get_issue(db, issue_id)
    if issue.reported_by != current_user.id and current_user.role.value not in ["municipal_admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this issue")
    return issue_service.update_issue(db, issue_id, data, current_user.id)


@router.delete("/{issue_id}", response_model=dict)
def delete_issue(
    issue_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete an issue (admin only)."""
    issue = issue_service.get_issue(db, issue_id)
    db.delete(issue)
    db.commit()
    return success_response(message="Issue deleted")


@router.post("/{issue_id}/assign", response_model=IssueResponse)
def assign_issue(
    issue_id: int,
    data: IssueAssign,
    current_user: User = Depends(require_department_head),
    db: Session = Depends(get_db),
):
    """Assign an issue to a worker."""
    return issue_service.assign_issue(db, issue_id, data.assigned_to, data.department_id, current_user.id)


@router.post("/{issue_id}/status", response_model=IssueResponse)
def update_status(
    issue_id: int,
    data: IssueStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update issue status."""
    return issue_service.change_status(db, issue_id, data.status, current_user.id, data.comment)


@router.get("/{issue_id}/timeline", response_model=dict)
def issue_timeline(
    issue_id: int,
    db: Session = Depends(get_db),
):
    """Get the audit trail / timeline for an issue."""
    from backend.models.audit_log import AuditLog
    logs = db.query(AuditLog).filter(
        AuditLog.entity_type == "issue",
        AuditLog.entity_id == issue_id,
    ).order_by(AuditLog.timestamp).all()
    timeline = [{"action": l.action, "timestamp": l.timestamp.isoformat(), "user_id": l.user_id} for l in logs]
    return success_response(timeline)
