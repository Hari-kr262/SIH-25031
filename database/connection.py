"""Database connection utilities and session management."""

from config.database import engine, Base, SessionLocal, get_db


def init_db():
    """Create all database tables."""
    import backend.models as _models  # registers all ORM models with SQLAlchemy metadata
    del _models  # imported for side-effects only
    Base.metadata.create_all(bind=engine)


__all__ = ["engine", "Base", "SessionLocal", "get_db", "init_db"]
