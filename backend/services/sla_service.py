"""SLA monitoring service."""

from typing import List, Dict
from sqlalchemy.orm import Session

from backend.models.issue import Issue, IssueStatus
from backend.models.sla_config import SLAConfig
from backend.utils.time_utils import get_elapsed_percent, is_overdue, now_utc


class SLAService:
    """Monitors SLA compliance for civic issues."""

    def get_at_risk_issues(self, db: Session, threshold: float = 75.0) -> List[Dict]:
        """Return issues approaching their SLA deadline."""
        active_statuses = [IssueStatus.pending, IssueStatus.verified,
                           IssueStatus.assigned, IssueStatus.in_progress]
        issues = db.query(Issue).filter(
            Issue.status.in_(active_statuses),
            Issue.deadline.isnot(None),
        ).all()

        at_risk = []
        for issue in issues:
            pct = get_elapsed_percent(issue.created_at, issue.deadline)
            if pct >= threshold and not is_overdue(issue.deadline):
                at_risk.append({
                    "issue_id": issue.id,
                    "title": issue.title,
                    "elapsed_percent": pct,
                    "deadline": issue.deadline.isoformat(),
                    "status": issue.status.value,
                })
        return at_risk

    def get_breached_issues(self, db: Session) -> List[Issue]:
        """Return issues that have exceeded their SLA deadline."""
        active_statuses = [IssueStatus.pending, IssueStatus.verified,
                           IssueStatus.assigned, IssueStatus.in_progress]
        return db.query(Issue).filter(
            Issue.status.in_(active_statuses),
            Issue.deadline < now_utc(),
        ).all()

    def escalate_overdue(self, db: Session) -> int:
        """Escalate all overdue issues. Returns count escalated."""
        overdue = self.get_breached_issues(db)
        count = 0
        for issue in overdue:
            if issue.status != IssueStatus.escalated:
                issue.status = IssueStatus.escalated
                count += 1
        db.commit()
        return count


sla_service = SLAService()
