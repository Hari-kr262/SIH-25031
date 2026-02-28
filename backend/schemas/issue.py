"""Pydantic schemas for Issue model."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from backend.models.issue import IssueCategory, IssuePriority, IssueStatus


class IssueCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: IssueCategory = IssueCategory.other
    priority: IssuePriority = IssuePriority.medium
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    ward: Optional[str] = None
    photo_url: Optional[str] = None
    is_anonymous: bool = False


class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[IssueCategory] = None
    priority: Optional[IssuePriority] = None
    status: Optional[IssueStatus] = None
    address: Optional[str] = None
    ward: Optional[str] = None
    assigned_to: Optional[int] = None
    department_id: Optional[int] = None
    estimated_cost: Optional[float] = None


class IssueResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: IssueCategory
    priority: IssuePriority
    status: IssueStatus
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    ward: Optional[str] = None
    photo_url: Optional[str] = None
    reported_by: int
    assigned_to: Optional[int] = None
    department_id: Optional[int] = None
    upvotes: int = 0
    downvotes: int = 0
    is_anonymous: bool = False
    ai_category_confidence: Optional[float] = None
    ai_urgency_score: Optional[float] = None
    is_ai_flagged_fake: bool = False
    deadline: Optional[datetime] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class IssueListResponse(BaseModel):
    items: List[IssueResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class IssueAssign(BaseModel):
    assigned_to: int
    department_id: Optional[int] = None


class IssueStatusUpdate(BaseModel):
    status: IssueStatus
    comment: Optional[str] = None
