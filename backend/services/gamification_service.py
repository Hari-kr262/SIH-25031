"""Gamification service — points, levels, badges."""

from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.models.badge import Badge, UserBadge
from config.constants import CITIZEN_LEVELS, get_level_for_points


class GamificationService:
    """Manages points, levels, and badge awards."""

    def add_points(self, db: Session, user_id: int, points: int) -> User:
        """Add points to a user and recalculate level."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user.points = max(0, user.points + points)
        user.level = self._calculate_level(user.points)
        db.commit()
        db.refresh(user)
        self._check_badges(db, user)
        return user

    def _calculate_level(self, points: int) -> int:
        """Return level index (1-based) for a given points total."""
        for i, level in enumerate(CITIZEN_LEVELS):
            if level["max"] is None or points <= level["max"]:
                return i + 1
        return len(CITIZEN_LEVELS)

    def _check_badges(self, db: Session, user: User):
        """Award any newly earned badges."""
        all_badges = db.query(Badge).all()
        earned_ids = {ub.badge_id for ub in db.query(UserBadge).filter_by(user_id=user.id).all()}

        for badge in all_badges:
            if badge.id in earned_ids:
                continue
            if self._criteria_met(db, user, badge.criteria or ""):
                ub = UserBadge(user_id=user.id, badge_id=badge.id)
                db.add(ub)
        db.commit()

    def _criteria_met(self, db: Session, user: User, criteria: str) -> bool:
        """Evaluate a criteria string against user stats."""
        from backend.models.issue import Issue
        if "total_points >=" in criteria:
            threshold = int(criteria.split(">=")[1].strip())
            return user.points >= threshold
        if "reports_count >=" in criteria:
            threshold = int(criteria.split(">=")[1].strip())
            count = db.query(Issue).filter_by(reported_by=user.id).count()
            return count >= threshold
        return False

    def get_leaderboard(self, db: Session, limit: int = 20) -> List[User]:
        """Return top users by points."""
        return db.query(User).filter(User.is_active == True).order_by(
            User.points.desc()
        ).limit(limit).all()

    def get_user_badges(self, db: Session, user_id: int) -> List[Badge]:
        """Return all badges earned by a user."""
        user_badge_ids = [ub.badge_id for ub in
                         db.query(UserBadge).filter_by(user_id=user_id).all()]
        return db.query(Badge).filter(Badge.id.in_(user_badge_ids)).all()


gamification_service = GamificationService()
