"""Vote routes: upvote, downvote, remove, count."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.user import User
from backend.models.vote import VoteType
from backend.services.voting_service import voting_service
from backend.middleware.auth_middleware import get_current_user
from backend.utils.response_utils import success_response

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/upvote/{issue_id}", response_model=dict)
def upvote(
    issue_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upvote an issue."""
    vote = voting_service.cast_vote(db, current_user.id, issue_id, VoteType.up)
    return success_response({"vote_id": vote.id}, "Upvoted successfully")


@router.post("/downvote/{issue_id}", response_model=dict)
def downvote(
    issue_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Downvote an issue."""
    vote = voting_service.cast_vote(db, current_user.id, issue_id, VoteType.down)
    return success_response({"vote_id": vote.id}, "Downvoted successfully")


@router.delete("/remove/{issue_id}", response_model=dict)
def remove_vote(
    issue_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove vote from an issue."""
    voting_service.remove_vote(db, current_user.id, issue_id)
    return success_response(message="Vote removed")


@router.get("/count/{issue_id}", response_model=dict)
def vote_count(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get vote counts and current user's vote for an issue."""
    from backend.models.issue import Issue
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    user_vote = voting_service.get_user_vote(db, current_user.id, issue_id)
    return success_response({
        "issue_id": issue_id,
        "upvotes": issue.upvotes if issue else 0,
        "downvotes": issue.downvotes if issue else 0,
        "user_vote": user_vote.vote_type.value if user_vote else None,
    })
