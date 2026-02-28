"""Gamification routes: stats, leaderboard, badges."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.user import User
from backend.services.gamification_service import gamification_service
from backend.middleware.auth_middleware import get_current_user
from backend.utils.response_utils import success_response
from config.constants import get_level_for_points

router = APIRouter(prefix="/gamification", tags=["Gamification"])


@router.get("/stats", response_model=dict)
def my_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current user's gamification stats."""
    badges = gamification_service.get_user_badges(db, current_user.id)
    level_info = get_level_for_points(current_user.points)
    return success_response({
        "user_id": current_user.id,
        "points": current_user.points,
        "level": current_user.level,
        "level_name": level_info["name"],
        "level_icon": level_info["icon"],
        "badges_count": len(badges),
        "badges": [{"name": b.name, "icon": b.icon, "description": b.description} for b in badges],
    })


@router.get("/leaderboard", response_model=dict)
def leaderboard(
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
):
    """Get top users by points."""
    users = gamification_service.get_leaderboard(db, limit=limit)
    return success_response([
        {
            "rank": i + 1,
            "user_id": u.id,
            "full_name": u.full_name,
            "points": u.points,
            "level": u.level,
            "avatar_url": u.avatar_url,
        }
        for i, u in enumerate(users)
    ])


@router.get("/badges", response_model=dict)
def all_badges(db: Session = Depends(get_db)):
    """Get all available badges."""
    from backend.models.badge import Badge
    badges = db.query(Badge).all()
    return success_response([
        {"id": b.id, "name": b.name, "icon": b.icon, "description": b.description,
         "points_required": b.points_required}
        for b in badges
    ])


@router.get("/badges/mine", response_model=dict)
def my_badges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get badges earned by the current user."""
    badges = gamification_service.get_user_badges(db, current_user.id)
    return success_response([
        {"name": b.name, "icon": b.icon, "description": b.description}
        for b in badges
    ])
