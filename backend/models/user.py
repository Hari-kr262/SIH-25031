"""User model — all 6 roles: citizen, volunteer, field_worker, department_head, municipal_admin, super_admin."""

import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from config.database import Base


class UserRole(str, enum.Enum):
    citizen = "citizen"
    volunteer = "volunteer"
    field_worker = "field_worker"
    department_head = "department_head"
    municipal_admin = "municipal_admin"
    super_admin = "super_admin"


class User(Base):
    """Represents a system user with role-based access control."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.citizen)

    # Department linkage (for department_head and field_worker)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    assigned_area = Column(String(200), nullable=True)

    # Hierarchical reporting
    reports_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Volunteer specific
    is_trusted_volunteer = Column(Boolean, default=False)

    # Gamification
    points = Column(Integer, default=0, nullable=False)
    level = Column(Integer, default=1, nullable=False)

    # Preferences
    preferred_language = Column(String(10), default="en")

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

    # Relationships
    department = relationship("Department", back_populates="members", foreign_keys=[department_id])
    manager = relationship("User", remote_side=[id], foreign_keys=[reports_to])

    reported_issues = relationship("Issue", back_populates="reporter",
                                   foreign_keys="Issue.reported_by")
    assigned_issues = relationship("Issue", back_populates="assignee",
                                   foreign_keys="Issue.assigned_to")
    votes = relationship("Vote", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    user_badges = relationship("UserBadge", back_populates="user")
    media_uploads = relationship("IssueMedia", back_populates="uploader")
    resolutions = relationship("Resolution", back_populates="worker")
    audit_logs = relationship("AuditLog", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"
