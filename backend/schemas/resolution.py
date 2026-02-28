"""Pydantic schemas for issue resolutions."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, ConfigDict


class ResolutionCreate(BaseModel):
    issue_id: int
    proof_video_url: Optional[str] = None
    proof_photo_url: Optional[str] = None
    description: Optional[str] = None
    geo_lat: Optional[float] = None
    geo_lng: Optional[float] = None


class ResolutionVerify(BaseModel):
    citizen_verified: bool
    citizen_rating: Optional[int] = None
    citizen_feedback: Optional[str] = None

    @field_validator("citizen_rating")
    @classmethod
    def validate_rating(cls, v):
        if v is not None and not (1 <= v <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return v


class ResolutionResponse(BaseModel):
    id: int
    issue_id: int
    worker_id: int
    proof_video_url: Optional[str] = None
    proof_photo_url: Optional[str] = None
    description: Optional[str] = None
    geo_lat: Optional[float] = None
    geo_lng: Optional[float] = None
    citizen_verified: Optional[bool] = None
    citizen_rating: Optional[int] = None
    citizen_feedback: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
