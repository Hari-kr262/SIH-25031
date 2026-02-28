"""Admin routes: user management, departments, announcements."""

from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.user import User, UserRole
from backend.models.department import Department
from backend.models.announcement import Announcement
from backend.middleware.rbac_middleware import require_admin, require_super_admin
from backend.utils.response_utils import success_response, paginated_response

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=dict)
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db),
):
    """List all users with optional filters."""
    query = db.query(User)
    if role:
        try:
            query = query.filter(User.role == UserRole(role))
        except ValueError:
            pass
    if search:
        query = query.filter(
            (User.full_name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%"))
        )
    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()
    return paginated_response(
        [{"id": u.id, "name": u.full_name, "email": u.email, "role": u.role.value,
          "is_active": u.is_active, "points": u.points} for u in users],
        total, page, page_size
    )


@router.put("/users/{user_id}/toggle-active", response_model=dict)
def toggle_user_active(
    user_id: int,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db),
):
    """Activate or deactivate a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = not user.is_active
    db.commit()
    return success_response({"is_active": user.is_active}, f"User {'activated' if user.is_active else 'deactivated'}")


@router.get("/departments", response_model=dict)
def list_departments(
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db),
):
    """List all departments."""
    depts = db.query(Department).all()
    return success_response([
        {"id": d.id, "name": d.name, "description": d.description,
         "head_id": d.head_id, "is_active": d.is_active}
        for d in depts
    ])


@router.post("/departments", response_model=dict, status_code=201)
def create_department(
    name: str,
    description: str = "",
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db),
):
    """Create a new department."""
    dept = Department(name=name, description=description, is_active=True)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return success_response({"id": dept.id}, "Department created")


@router.post("/announcements", response_model=dict, status_code=201)
def create_announcement(
    title: str,
    content: str,
    target_role: Optional[str] = None,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db),
):
    """Create a system announcement."""
    ann = Announcement(
        title=title,
        content=content,
        created_by=current_user.id,
        target_role=target_role,
        is_active=True,
    )
    db.add(ann)
    db.commit()
    db.refresh(ann)
    return success_response({"id": ann.id}, "Announcement created")


@router.get("/announcements", response_model=dict)
def list_announcements(db: Session = Depends(get_db)):
    """List active announcements."""
    anns = db.query(Announcement).filter_by(is_active=True).order_by(
        Announcement.created_at.desc()
    ).all()
    return success_response([
        {"id": a.id, "title": a.title, "content": a.content,
         "target_role": a.target_role, "created_at": a.created_at.isoformat()}
        for a in anns
    ])


@router.get("/audit-logs", response_model=dict)
def audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db),
):
    """Get paginated audit logs."""
    from backend.services.audit_service import audit_service
    logs, total = audit_service.get_logs(db, page=page, page_size=page_size)
    return paginated_response(
        [{"id": l.id, "user_id": l.user_id, "action": l.action,
          "entity_type": l.entity_type, "timestamp": l.timestamp.isoformat()}
         for l in logs],
        total, page, page_size
    )
