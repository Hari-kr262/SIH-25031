"""AuditLog model — immutable action trail for compliance."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from config.database import Base


class AuditLog(Base):
    """Immutable log of all significant actions in the system."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)        # e.g. "issue.create"
    entity_type = Column(String(50), nullable=True)     # e.g. "issue"
    entity_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)               # JSON string
    ip_address = Column(String(45), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog id={self.id} action={self.action} user={self.user_id}>"
