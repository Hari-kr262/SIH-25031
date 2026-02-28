"""SLAConfig model — SLA deadline settings per issue category."""

from sqlalchemy import Column, Integer, Float, Enum as SAEnum
from config.database import Base
from backend.models.issue import IssueCategory


class SLAConfig(Base):
    """Service Level Agreement configuration per issue category."""

    __tablename__ = "sla_configs"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(SAEnum(IssueCategory), unique=True, nullable=False)
    deadline_hours = Column(Integer, nullable=False)             # Hours to resolve
    warning_threshold_percent = Column(Float, default=75.0)      # % elapsed before warning
    escalation_levels = Column(Integer, default=3)               # Number of escalation levels

    def __repr__(self):
        return f"<SLAConfig category={self.category} deadline={self.deadline_hours}h>"
