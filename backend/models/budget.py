"""Budget model — tracks departmental budget allocations and expenditures."""

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class Budget(Base):
    """Departmental budget allocation and spending tracker."""

    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    allocated_amount = Column(Float, nullable=False, default=0.0)
    spent_amount = Column(Float, nullable=False, default=0.0)
    fiscal_year = Column(Integer, nullable=False)

    # Relationships
    department = relationship("Department", back_populates="budgets")

    @property
    def remaining_amount(self):
        return self.allocated_amount - self.spent_amount

    @property
    def utilization_percent(self):
        if self.allocated_amount == 0:
            return 0
        return round((self.spent_amount / self.allocated_amount) * 100, 2)

    def __repr__(self):
        return f"<Budget dept={self.department_id} year={self.fiscal_year} allocated={self.allocated_amount}>"
