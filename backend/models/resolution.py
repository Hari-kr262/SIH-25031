"""Resolution model — proof of fix submitted by field workers."""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Float,
    ForeignKey, Text
)
from sqlalchemy.orm import relationship
from config.database import Base


class Resolution(Base):
    """Fix proof submitted by field workers for a civic issue."""

    __tablename__ = "resolutions"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=False, unique=True)
    worker_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Proof media
    proof_video_url = Column(String(500), nullable=True)
    proof_photo_url = Column(String(500), nullable=True)

    # Description
    description = Column(Text, nullable=True)

    # Geo-verification of fix location
    geo_lat = Column(Float, nullable=True)
    geo_lng = Column(Float, nullable=True)

    # Citizen verification
    citizen_verified = Column(Boolean, nullable=True)
    citizen_rating = Column(Integer, nullable=True)   # 1-5
    citizen_feedback = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)

    # Relationships
    issue = relationship("Issue", back_populates="resolution")
    worker = relationship("User", back_populates="resolutions")

    def __repr__(self):
        return f"<Resolution id={self.id} issue_id={self.issue_id} worker={self.worker_id}>"
