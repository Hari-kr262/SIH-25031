"""Pydantic schemas for notifications."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from backend.models.notification import NotificationType


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: NotificationType
    is_read: bool
    link: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    items: List[NotificationResponse]
    total: int
    unread_count: int
