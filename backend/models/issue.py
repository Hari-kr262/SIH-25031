"""Issue model — the core entity of the civic reporting system."""

import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Float,
    ForeignKey, Enum as SAEnum, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from config.database import Base


class IssueCategory(str, enum.Enum):
    pothole = "pothole"
    garbage = "garbage"
    streetlight = "streetlight"
    water_leak = "water_leak"
    drainage = "drainage"
    road_damage = "road_damage"
    illegal_dumping = "illegal_dumping"
    fallen_tree = "fallen_tree"
    sewage = "sewage"
    public_property = "public_property"
    other = "other"


class IssuePriority(str, enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class IssueStatus(str, enum.Enum):
    pending = "pending"
    verified = "verified"
    assigned = "assigned"
    in_progress = "in_progress"
    fix_uploaded = "fix_uploaded"
    resolved = "resolved"
    rejected = "rejected"
    escalated = "escalated"
    closed = "closed"


class Issue(Base):
    """Represents a civic issue reported by a citizen."""

    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)

    category = Column(SAEnum(IssueCategory), nullable=False, default=IssueCategory.other)
    priority = Column(SAEnum(IssuePriority), nullable=False, default=IssuePriority.medium)
    status = Column(SAEnum(IssueStatus), nullable=False, default=IssueStatus.pending)

    # Location
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String(500), nullable=True)
    ward = Column(String(100), nullable=True)

    # Media
    photo_url = Column(String(500), nullable=True)

    # Relationships (FKs)
    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    # Social
    upvotes = Column(Integer, default=0, nullable=False)
    downvotes = Column(Integer, default=0, nullable=False)
    is_anonymous = Column(Boolean, default=False)

    # AI fields
    ai_category_confidence = Column(Float, nullable=True)
    ai_urgency_score = Column(Float, nullable=True)
    is_ai_flagged_fake = Column(Boolean, default=False)

    # SLA
    deadline = Column(DateTime, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    actual_cost = Column(Float, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    reporter = relationship("User", back_populates="reported_issues",
                            foreign_keys=[reported_by])
    assignee = relationship("User", back_populates="assigned_issues",
                            foreign_keys=[assigned_to])
    department = relationship("Department", back_populates="issues")
    media = relationship("IssueMedia", back_populates="issue",
                         cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="issue",
                         cascade="all, delete-orphan")
    resolution = relationship("Resolution", back_populates="issue",
                              uselist=False)
    comments = relationship("Comment", back_populates="issue",
                            cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Issue id={self.id} title={self.title[:30]} status={self.status}>"
