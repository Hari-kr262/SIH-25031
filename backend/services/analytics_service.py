"""Analytics service — aggregated statistics and insights."""

from datetime import timedelta
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from backend.models.issue import Issue, IssueStatus
from backend.models.resolution import Resolution
from backend.utils.time_utils import now_utc


class AnalyticsService:
    """Provides analytics data for dashboards and reports."""

    def get_overview_stats(self, db: Session) -> Dict[str, Any]:
        """Return high-level system statistics."""
        total = db.query(Issue).count()
        resolved = db.query(Issue).filter(Issue.status == IssueStatus.resolved).count()
        pending = db.query(Issue).filter(Issue.status == IssueStatus.pending).count()
        in_progress = db.query(Issue).filter(Issue.status == IssueStatus.in_progress).count()

        rate = round((resolved / total * 100), 2) if total > 0 else 0

        # Average resolution time
        resolved_issues = db.query(Issue, Resolution).join(
            Resolution, Issue.id == Resolution.issue_id
        ).filter(Resolution.citizen_verified == True).all()

        avg_hours = 0
        if resolved_issues:
            durations = []
            for issue, res in resolved_issues:
                if issue.created_at and res.created_at:
                    delta = res.created_at - issue.created_at
                    durations.append(delta.total_seconds() / 3600)
            avg_hours = round(sum(durations) / len(durations), 2) if durations else 0

        return {
            "total_issues": total,
            "resolved_issues": resolved,
            "pending_issues": pending,
            "in_progress_issues": in_progress,
            "resolution_rate": rate,
            "avg_resolution_hours": avg_hours,
        }

    def get_issues_by_category(self, db: Session) -> Dict[str, int]:
        """Return issue count per category."""
        rows = db.query(Issue.category, func.count(Issue.id)).group_by(Issue.category).all()
        return {row[0].value: row[1] for row in rows}

    def get_issues_by_status(self, db: Session) -> Dict[str, int]:
        """Return issue count per status."""
        rows = db.query(Issue.status, func.count(Issue.id)).group_by(Issue.status).all()
        return {row[0].value: row[1] for row in rows}

    def get_top_wards(self, db: Session, limit: int = 10) -> List[Dict]:
        """Return wards with most reported issues."""
        rows = (
            db.query(Issue.ward, func.count(Issue.id).label("count"))
            .filter(Issue.ward.isnot(None))
            .group_by(Issue.ward)
            .order_by(desc("count"))
            .limit(limit)
            .all()
        )
        return [{"ward": r[0], "count": r[1]} for r in rows]

    def get_trend_data(self, db: Session, days: int = 30) -> List[Dict]:
        """Return daily issue counts for the last N days."""
        start_date = now_utc() - timedelta(days=days)
        rows = (
            db.query(
                func.date(Issue.created_at).label("date"),
                func.count(Issue.id).label("count"),
            )
            .filter(Issue.created_at >= start_date)
            .group_by(func.date(Issue.created_at))
            .order_by("date")
            .all()
        )
        return [{"date": str(r[0]), "count": r[1]} for r in rows]

    def get_department_performance(self, db: Session) -> List[Dict]:
        """Return performance metrics per department."""
        from backend.models.department import Department
        departments = db.query(Department).filter(Department.is_active == True).all()
        results = []
        for dept in departments:
            total = db.query(Issue).filter(Issue.department_id == dept.id).count()
            resolved = db.query(Issue).filter(
                Issue.department_id == dept.id,
                Issue.status == IssueStatus.resolved
            ).count()
            results.append({
                "department_id": dept.id,
                "department_name": dept.name,
                "total_issues": total,
                "resolved_issues": resolved,
                "resolution_rate": round(resolved / total * 100, 2) if total > 0 else 0,
            })
        return results


analytics_service = AnalyticsService()
