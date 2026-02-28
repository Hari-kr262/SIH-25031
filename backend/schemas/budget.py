"""Pydantic schemas for budget management."""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class BudgetAllocate(BaseModel):
    department_id: int
    allocated_amount: float
    fiscal_year: int


class BudgetExpense(BaseModel):
    issue_id: int
    amount: float
    description: Optional[str] = None


class BudgetResponse(BaseModel):
    id: int
    department_id: int
    allocated_amount: float
    spent_amount: float
    fiscal_year: int
    remaining_amount: float
    utilization_percent: float

    model_config = ConfigDict(from_attributes=True)
