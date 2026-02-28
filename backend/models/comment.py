"""Comment model — citizens and officials can comment on issues."""

from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from config.database import Base


class Comment(Base):
    """Discussion threads on civic issues."""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)  # Internal staff notes

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    issue = relationship("Issue", back_populates="comments")
    user = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"<Comment id={self.id} issue={self.issue_id} user={self.user_id}>"
