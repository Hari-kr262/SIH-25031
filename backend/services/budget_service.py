"""Budget management service."""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.budget import Budget
from backend.models.issue import Issue


class BudgetService:
    """Manages departmental budget allocation and expenditure tracking."""

    def get_department_budget(self, db: Session, department_id: int, fiscal_year: int) -> Optional[Budget]:
        """Get budget for a department in a fiscal year."""
        return db.query(Budget).filter_by(
            department_id=department_id, fiscal_year=fiscal_year
        ).first()

    def allocate_budget(self, db: Session, department_id: int, amount: float, fiscal_year: int) -> Budget:
        """Create or update budget allocation for a department."""
        budget = self.get_department_budget(db, department_id, fiscal_year)
        if budget:
            budget.allocated_amount = amount
        else:
            budget = Budget(
                department_id=department_id,
                allocated_amount=amount,
                spent_amount=0.0,
                fiscal_year=fiscal_year,
            )
            db.add(budget)
        db.commit()
        db.refresh(budget)
        return budget

    def record_expense(self, db: Session, department_id: int, amount: float, issue_id: int, fiscal_year: int) -> Budget:
        """Record an expense against a department budget."""
        budget = self.get_department_budget(db, department_id, fiscal_year)
        if not budget:
            raise HTTPException(status_code=404, detail="Budget not found")
        if budget.spent_amount + amount > budget.allocated_amount:
            raise HTTPException(status_code=400, detail="Expense exceeds budget allocation")

        budget.spent_amount += amount

        # Update actual cost on issue
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if issue:
            issue.actual_cost = (issue.actual_cost or 0) + amount

        db.commit()
        db.refresh(budget)
        return budget

    def get_all_budgets(self, db: Session, fiscal_year: Optional[int] = None) -> List[Budget]:
        """Get all budgets, optionally filtered by fiscal year."""
        query = db.query(Budget)
        if fiscal_year:
            query = query.filter(Budget.fiscal_year == fiscal_year)
        return query.all()


budget_service = BudgetService()
