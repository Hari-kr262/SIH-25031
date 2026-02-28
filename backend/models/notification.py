"""Notification model — in-app notifications for users."""

import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import relationship
from config.database import Base


class NotificationType(str, enum.Enum):
    issue_update = "issue_update"
    issue_assigned = "issue_assigned"
    issue_resolved = "issue_resolved"
    vote_received = "vote_received"
    badge_earned = "badge_earned"
    sla_warning = "sla_warning"
    sla_breached = "sla_breached"
    announcement = "announcement"
    comment = "comment"
    system = "system"


class Notification(Base):
    """In-app notification records for users."""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(SAEnum(NotificationType), nullable=False, default=NotificationType.system)
    is_read = Column(Boolean, default=False)
    link = Column(String(500), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification id={self.id} user={self.user_id} read={self.is_read}>"
