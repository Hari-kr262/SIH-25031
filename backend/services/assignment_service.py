"""Assignment service — smart issue-to-worker assignment."""

from typing import Optional, List
from sqlalchemy.orm import Session
from backend.models.user import User, UserRole
from backend.models.issue import Issue, IssueStatus


class AssignmentService:
    """Handles intelligent assignment of issues to field workers."""

    def get_available_workers(self, db: Session, department_id: Optional[int] = None) -> List[User]:
        """Return active field workers, optionally filtered by department."""
        query = db.query(User).filter(
            User.role == UserRole.field_worker,
            User.is_active == True,
        )
        if department_id:
            query = query.filter(User.department_id == department_id)
        return query.all()

    def get_worker_workload(self, db: Session, worker_id: int) -> int:
        """Return count of active issues assigned to a worker."""
        return db.query(Issue).filter(
            Issue.assigned_to == worker_id,
            Issue.status.in_([IssueStatus.assigned, IssueStatus.in_progress]),
        ).count()

    def auto_assign(self, db: Session, issue: Issue) -> Optional[User]:
        """Auto-assign to least busy worker in the same department."""
        workers = self.get_available_workers(db, issue.department_id)
        if not workers:
            return None

        # Find least busy worker
        best_worker = min(workers, key=lambda w: self.get_worker_workload(db, w.id))
        issue.assigned_to = best_worker.id
        issue.status = IssueStatus.assigned
        db.commit()
        return best_worker


assignment_service = AssignmentService()
