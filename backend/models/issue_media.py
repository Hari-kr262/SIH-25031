"""IssueMedia model — stores media files attached to issues."""

import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SAEnum, DateTime
from sqlalchemy.orm import relationship
from config.database import Base


class MediaType(str, enum.Enum):
    photo = "photo"
    video = "video"
    document = "document"
    audio = "audio"


class IssueMedia(Base):
    """Media attachments for civic issues."""

    __tablename__ = "issue_media"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=False)
    media_url = Column(String(500), nullable=False)
    media_type = Column(SAEnum(MediaType), nullable=False, default=MediaType.photo)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    issue = relationship("Issue", back_populates="media")
    uploader = relationship("User", back_populates="media_uploads")

    def __repr__(self):
        return f"<IssueMedia id={self.id} issue_id={self.issue_id} type={self.media_type}>"
