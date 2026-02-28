"""Department model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from config.database import Base


class Department(Base):
    """Represents a city department (Roads, Water, etc.)."""

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    head_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    head = relationship("User", foreign_keys=[head_id], post_update=True)
    members = relationship("User", back_populates="department",
                           foreign_keys="User.department_id")
    issues = relationship("Issue", back_populates="department")
    budgets = relationship("Budget", back_populates="department")

    def __repr__(self):
        return f"<Department id={self.id} name={self.name}>"
