"""Pydantic schemas for voting."""

from pydantic import BaseModel
from backend.models.vote import VoteType


class VoteCreate(BaseModel):
    issue_id: int
    vote_type: VoteType


class VoteResponse(BaseModel):
    id: int
    user_id: int
    issue_id: int
    vote_type: VoteType

    class Config:
        from_attributes = True


class VoteCount(BaseModel):
    issue_id: int
    upvotes: int
    downvotes: int
    user_vote: VoteType | None = None
