"""Pydantic schemas for comments."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    issue_id: int
    content: str
    is_internal: bool = False


class CommentUpdate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    issue_id: int
    user_id: int
    content: str
    is_internal: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
