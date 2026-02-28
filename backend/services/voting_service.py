"""Voting service — upvote/downvote issues."""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.vote import Vote, VoteType
from backend.models.issue import Issue
from backend.services.gamification_service import gamification_service
from config.constants import Points


class VotingService:
    """Handles upvote/downvote logic for civic issues."""

    def cast_vote(self, db: Session, user_id: int, issue_id: int, vote_type: VoteType) -> Vote:
        """Cast or update a vote. One vote per user per issue."""
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found")

        existing = db.query(Vote).filter_by(user_id=user_id, issue_id=issue_id).first()
        if existing:
            if existing.vote_type == vote_type:
                raise HTTPException(status_code=400, detail="Already voted with same type")
            # Change vote
            if existing.vote_type == VoteType.up:
                issue.upvotes = max(0, issue.upvotes - 1)
            else:
                issue.downvotes = max(0, issue.downvotes - 1)
            existing.vote_type = vote_type
        else:
            existing = Vote(user_id=user_id, issue_id=issue_id, vote_type=vote_type)
            db.add(existing)

        if vote_type == VoteType.up:
            issue.upvotes += 1
            gamification_service.add_points(db, user_id, Points.UPVOTE)
        else:
            issue.downvotes += 1

        db.commit()
        db.refresh(existing)
        return existing

    def remove_vote(self, db: Session, user_id: int, issue_id: int) -> bool:
        """Remove a user's vote from an issue."""
        vote = db.query(Vote).filter_by(user_id=user_id, issue_id=issue_id).first()
        if not vote:
            raise HTTPException(status_code=404, detail="Vote not found")

        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if issue:
            if vote.vote_type == VoteType.up:
                issue.upvotes = max(0, issue.upvotes - 1)
            else:
                issue.downvotes = max(0, issue.downvotes - 1)

        db.delete(vote)
        db.commit()
        return True

    def get_user_vote(self, db: Session, user_id: int, issue_id: int):
        """Get a user's vote on a specific issue."""
        return db.query(Vote).filter_by(user_id=user_id, issue_id=issue_id).first()


voting_service = VotingService()
