"""Notification routes: list, read, read-all, unread-count."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.user import User
from backend.services.notification_service import notification_service
from backend.middleware.auth_middleware import get_current_user
from backend.utils.response_utils import success_response

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=dict)
def list_notifications(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    unread_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get paginated notifications for the current user."""
    items = notification_service.get_user_notifications(
        db, current_user.id, unread_only=unread_only, page=page, page_size=page_size
    )
    unread = notification_service.get_unread_count(db, current_user.id)
    return success_response({"items": [i.__dict__ for i in items], "unread_count": unread})


@router.post("/{notification_id}/read", response_model=dict)
def mark_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a notification as read."""
    notification_service.mark_read(db, notification_id, current_user.id)
    return success_response(message="Marked as read")


@router.post("/read-all", response_model=dict)
def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark all notifications as read."""
    count = notification_service.mark_all_read(db, current_user.id)
    return success_response({"updated": count}, "All notifications marked as read")


@router.get("/unread-count", response_model=dict)
def unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get count of unread notifications."""
    count = notification_service.get_unread_count(db, current_user.id)
    return success_response({"unread_count": count})
