"""Issue service — CRUD operations for civic issues."""

from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, func
from fastapi import HTTPException, status

from backend.models.issue import Issue, IssueStatus, IssueCategory, IssuePriority
from backend.models.sla_config import SLAConfig
from backend.schemas.issue import IssueCreate, IssueUpdate
from backend.services.audit_service import log_action
from config.constants import CATEGORY_TO_DEPARTMENT


class IssueService:
    """Business logic for civic issue management."""

    def create_issue(self, db: Session, issue_data: IssueCreate, reporter_id: int) -> Issue:
        """Create a new civic issue report."""
        # Look up department for category
        dept_name = CATEGORY_TO_DEPARTMENT.get(issue_data.category.value)
        dept_id = None
        if dept_name:
            from backend.models.department import Department
            dept = db.query(Department).filter_by(name=dept_name).first()
            if dept:
                dept_id = dept.id

        # Determine SLA deadline
        sla = db.query(SLAConfig).filter_by(category=issue_data.category).first()
        deadline = None
        if sla:
            deadline = datetime.utcnow() + timedelta(hours=sla.deadline_hours)

        issue = Issue(
            title=issue_data.title,
            description=issue_data.description,
            category=issue_data.category,
            priority=issue_data.priority,
            status=IssueStatus.pending,
            latitude=issue_data.latitude,
            longitude=issue_data.longitude,
            address=issue_data.address,
            ward=issue_data.ward,
            photo_url=issue_data.photo_url,
            reported_by=reporter_id,
            department_id=dept_id,
            is_anonymous=issue_data.is_anonymous,
            deadline=deadline,
        )
        db.add(issue)
        db.commit()
        db.refresh(issue)
        log_action(db, reporter_id, "issue.create", "issue", issue.id)
        return issue

    def get_issue(self, db: Session, issue_id: int) -> Issue:
        """Get a single issue by ID."""
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found")
        return issue

    def list_issues(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        status: Optional[IssueStatus] = None,
        category: Optional[IssueCategory] = None,
        priority: Optional[IssuePriority] = None,
        department_id: Optional[int] = None,
        reporter_id: Optional[int] = None,
        ward: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Issue], int]:
        """List issues with filters and pagination."""
        query = db.query(Issue)

        if status:
            query = query.filter(Issue.status == status)
        if category:
            query = query.filter(Issue.category == category)
        if priority:
            query = query.filter(Issue.priority == priority)
        if department_id:
            query = query.filter(Issue.department_id == department_id)
        if reporter_id:
            query = query.filter(Issue.reported_by == reporter_id)
        if ward:
            query = query.filter(Issue.ward.ilike(f"%{ward}%"))
        if search:
            query = query.filter(
                or_(
                    Issue.title.ilike(f"%{search}%"),
                    Issue.description.ilike(f"%{search}%"),
                    Issue.address.ilike(f"%{search}%"),
                )
            )

        total = query.count()
        items = (
            query.order_by(desc(Issue.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return items, total

    def update_issue(self, db: Session, issue_id: int, update_data: IssueUpdate, user_id: int) -> Issue:
        """Update an issue."""
        issue = self.get_issue(db, issue_id)
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(issue, field, value)
        issue.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(issue)
        log_action(db, user_id, "issue.update", "issue", issue.id)
        return issue

    def change_status(self, db: Session, issue_id: int, new_status: IssueStatus, user_id: int, comment: Optional[str] = None) -> Issue:
        """Change issue status and optionally add a comment."""
        issue = self.get_issue(db, issue_id)
        old_status = issue.status
        issue.status = new_status
        issue.updated_at = datetime.utcnow()

        if comment:
            from backend.models.comment import Comment
            c = Comment(issue_id=issue_id, user_id=user_id, content=comment, is_internal=True)
            db.add(c)

        db.commit()
        db.refresh(issue)
        log_action(db, user_id, f"issue.status.{new_status.value}", "issue", issue_id,
                   details=f"from={old_status.value}")
        return issue

    def assign_issue(self, db: Session, issue_id: int, assigned_to: int, department_id: Optional[int], user_id: int) -> Issue:
        """Assign an issue to a worker and optionally a department."""
        issue = self.get_issue(db, issue_id)
        issue.assigned_to = assigned_to
        if department_id:
            issue.department_id = department_id
        issue.status = IssueStatus.assigned
        issue.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(issue)
        log_action(db, user_id, "issue.assign", "issue", issue_id,
                   details=f"assigned_to={assigned_to}")
        return issue

    def get_trending(self, db: Session, limit: int = 10) -> List[Issue]:
        """Get trending issues ordered by upvotes."""
        return (
            db.query(Issue)
            .filter(Issue.status.notin_([IssueStatus.closed, IssueStatus.rejected]))
            .order_by(desc(Issue.upvotes), desc(Issue.created_at))
            .limit(limit)
            .all()
        )

    def get_nearby(self, db: Session, lat: float, lng: float, radius_km: float = 2.0) -> List[Issue]:
        """Get issues near a location (approximate bounding box query)."""
        from backend.utils.geo_utils import get_bounding_box, haversine_distance
        min_lat, max_lat, min_lng, max_lng = get_bounding_box(lat, lng, radius_km)
        issues = (
            db.query(Issue)
            .filter(
                Issue.latitude.between(min_lat, max_lat),
                Issue.longitude.between(min_lng, max_lng),
                Issue.status.notin_([IssueStatus.closed]),
            )
            .all()
        )
        # Filter by actual Haversine distance
        return [i for i in issues if i.latitude and i.longitude and
                haversine_distance(lat, lng, i.latitude, i.longitude) <= radius_km]


issue_service = IssueService()
