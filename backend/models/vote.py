"""Vote model — upvotes/downvotes on issues (one vote per user per issue)."""

import enum
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Enum as SAEnum, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from config.database import Base


class VoteType(str, enum.Enum):
    up = "up"
    down = "down"


class Vote(Base):
    """Records citizen votes on issues."""

    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=False)
    vote_type = Column(SAEnum(VoteType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "issue_id", name="uq_user_issue_vote"),
    )

    # Relationships
    user = relationship("User", back_populates="votes")
    issue = relationship("Issue", back_populates="votes")

    def __repr__(self):
        return f"<Vote id={self.id} user={self.user_id} issue={self.issue_id} type={self.vote_type}>"
