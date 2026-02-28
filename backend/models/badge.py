"""Badge and UserBadge models — gamification reward system."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from config.database import Base


class Badge(Base):
    """Defines available achievement badges."""

    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(10), nullable=True)
    points_required = Column(Integer, default=0)
    criteria = Column(String(255), nullable=True)  # Machine-readable criteria string

    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")

    def __repr__(self):
        return f"<Badge id={self.id} name={self.name}>"


class UserBadge(Base):
    """Tracks which badges users have earned."""

    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "badge_id", name="uq_user_badge"),
    )

    # Relationships
    user = relationship("User", back_populates="user_badges")
    badge = relationship("Badge", back_populates="user_badges")

    def __repr__(self):
        return f"<UserBadge user={self.user_id} badge={self.badge_id}>"
