"""Notification service — create and manage user notifications."""

from typing import Optional, List
from sqlalchemy.orm import Session
from backend.models.notification import Notification, NotificationType


class NotificationService:
    """Manages in-app notification creation and delivery."""

    def create_notification(
        self,
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notif_type: str = "system",
        link: Optional[str] = None,
    ) -> Notification:
        """Create an in-app notification for a user."""
        try:
            ntype = NotificationType(notif_type)
        except ValueError:
            ntype = NotificationType.system

        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=ntype,
            link=link,
            is_read=False,
        )
        db.add(notif)
        db.commit()
        db.refresh(notif)
        return notif

    def get_user_notifications(
        self, db: Session, user_id: int, unread_only: bool = False, page: int = 1, page_size: int = 20
    ) -> List[Notification]:
        """Get paginated notifications for a user."""
        query = db.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.order_by(Notification.timestamp.desc()).offset((page-1)*page_size).limit(page_size).all()

    def mark_read(self, db: Session, notification_id: int, user_id: int) -> bool:
        """Mark a single notification as read."""
        notif = db.query(Notification).filter_by(id=notification_id, user_id=user_id).first()
        if notif:
            notif.is_read = True
            db.commit()
            return True
        return False

    def mark_all_read(self, db: Session, user_id: int) -> int:
        """Mark all notifications as read for a user. Returns count updated."""
        count = db.query(Notification).filter_by(user_id=user_id, is_read=False).update({"is_read": True})
        db.commit()
        return count

    def get_unread_count(self, db: Session, user_id: int) -> int:
        """Return number of unread notifications."""
        return db.query(Notification).filter_by(user_id=user_id, is_read=False).count()


notification_service = NotificationService()
