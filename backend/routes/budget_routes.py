"""Budget routes: allocate, expense, report."""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.user import User
from backend.schemas.budget import BudgetAllocate, BudgetExpense
from backend.services.budget_service import budget_service
from backend.middleware.rbac_middleware import require_admin, require_department_head
from backend.utils.response_utils import success_response

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.get("/", response_model=dict)
def list_budgets(
    fiscal_year: Optional[int] = Query(None),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """List all department budgets."""
    year = fiscal_year or datetime.now(timezone.utc).year
    budgets = budget_service.get_all_budgets(db, fiscal_year=year)
    return success_response([
        {
            "id": b.id,
            "department_id": b.department_id,
            "allocated_amount": b.allocated_amount,
            "spent_amount": b.spent_amount,
            "remaining_amount": b.remaining_amount,
            "utilization_percent": b.utilization_percent,
            "fiscal_year": b.fiscal_year,
        }
        for b in budgets
    ])


@router.post("/allocate", response_model=dict, status_code=201)
def allocate_budget(
    data: BudgetAllocate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Allocate budget to a department."""
    budget = budget_service.allocate_budget(db, data.department_id, data.allocated_amount, data.fiscal_year)
    return success_response({"budget_id": budget.id}, "Budget allocated")


@router.post("/expense", response_model=dict)
def record_expense(
    data: BudgetExpense,
    current_user: User = Depends(require_department_head),
    db: Session = Depends(get_db),
):
    """Record an expense against department budget."""
    year = datetime.now(timezone.utc).year
    dept_id = current_user.department_id
    if not dept_id:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="User has no department assigned")
    budget = budget_service.record_expense(db, dept_id, data.amount, data.issue_id, year)
    return success_response({"remaining": budget.remaining_amount}, "Expense recorded")
