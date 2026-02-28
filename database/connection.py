"""Database connection utilities and session management."""

from config.database import engine, Base, SessionLocal, get_db


def init_db():
    """Create all database tables."""
    # Import all models so SQLAlchemy knows about them
    from backend.models import (  # noqa: F401
        User, Department, Issue, IssueMedia, Vote, Resolution,
        Comment, Notification, Badge, UserBadge, SLAConfig,
        Budget, AuditLog, Announcement,
    )
    Base.metadata.create_all(bind=engine)


__all__ = ["engine", "Base", "SessionLocal", "get_db", "init_db"]
