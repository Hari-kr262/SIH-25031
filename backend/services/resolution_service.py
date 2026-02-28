"""Resolution service — fix proof submission and citizen verification."""

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend.models.resolution import Resolution
from backend.models.issue import Issue, IssueStatus
from backend.schemas.resolution import ResolutionCreate, ResolutionVerify
from backend.services.gamification_service import gamification_service
from backend.services.notification_service import notification_service
from backend.services.audit_service import log_action
from backend.utils.time_utils import now_utc
from config.constants import Points


class ResolutionService:
    """Manages fix proof submission and citizen verification."""

    def submit_proof(self, db: Session, resolution_data: ResolutionCreate, worker_id: int) -> Resolution:
        """Field worker submits proof of fix."""
        issue = db.query(Issue).filter(Issue.id == resolution_data.issue_id).first()
        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found")
        if issue.assigned_to != worker_id:
            raise HTTPException(status_code=403, detail="Not authorized to submit proof for this issue")

        existing = db.query(Resolution).filter_by(issue_id=resolution_data.issue_id).first()
        if existing:
            # Update existing resolution
            for f, v in resolution_data.model_dump(exclude_unset=True).items():
                setattr(existing, f, v)
            db.commit()
            db.refresh(existing)
            resolution = existing
        else:
            resolution = Resolution(
                issue_id=resolution_data.issue_id,
                worker_id=worker_id,
                proof_video_url=resolution_data.proof_video_url,
                proof_photo_url=resolution_data.proof_photo_url,
                description=resolution_data.description,
                geo_lat=resolution_data.geo_lat,
                geo_lng=resolution_data.geo_lng,
            )
            db.add(resolution)

        issue.status = IssueStatus.fix_uploaded
        db.commit()
        if not existing:
            db.refresh(resolution)

        # Notify the reporter
        if issue.reported_by:
            notification_service.create_notification(
                db,
                user_id=issue.reported_by,
                title="Issue Fix Ready for Verification",
                message=f"The fix for '{issue.title}' has been uploaded. Please verify!",
                notif_type="issue_resolved",
                link=f"/issues/{issue.id}",
            )

        log_action(db, worker_id, "resolution.submit", "issue", issue.id)
        return resolution

    def verify_resolution(
        self, db: Session, issue_id: int, verify_data: ResolutionVerify, citizen_id: int
    ) -> Resolution:
        """Citizen verifies whether the fix is satisfactory."""
        resolution = db.query(Resolution).filter_by(issue_id=issue_id).first()
        if not resolution:
            raise HTTPException(status_code=404, detail="Resolution not found")

        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if issue.reported_by != citizen_id:
            raise HTTPException(status_code=403, detail="Only the reporter can verify this resolution")

        resolution.citizen_verified = verify_data.citizen_verified
        resolution.citizen_rating = verify_data.citizen_rating
        resolution.citizen_feedback = verify_data.citizen_feedback
        resolution.verified_at = now_utc()

        issue.status = IssueStatus.resolved if verify_data.citizen_verified else IssueStatus.in_progress
        db.commit()
        db.refresh(resolution)

        if verify_data.citizen_verified:
            gamification_service.add_points(db, citizen_id, Points.VERIFY_RESOLUTION)
            gamification_service.add_points(db, resolution.worker_id, Points.VOLUNTEER_FIX)

        log_action(db, citizen_id, "resolution.verify", "issue", issue_id)
        return resolution


resolution_service = ResolutionService()
