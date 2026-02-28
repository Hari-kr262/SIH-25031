"""Comment routes: CRUD comments on issues."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.user import User
from backend.models.comment import Comment
from backend.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from backend.middleware.auth_middleware import get_current_user
from backend.utils.response_utils import success_response

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=dict, status_code=201)
def add_comment(
    data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a comment to an issue."""
    comment = Comment(
        issue_id=data.issue_id,
        user_id=current_user.id,
        content=data.content,
        is_internal=data.is_internal,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return success_response({"comment_id": comment.id}, "Comment added")


@router.get("/issue/{issue_id}", response_model=dict)
def get_issue_comments(issue_id: int, db: Session = Depends(get_db)):
    """Get all comments for an issue."""
    comments = db.query(Comment).filter(
        Comment.issue_id == issue_id,
        Comment.is_internal == False
    ).order_by(Comment.created_at).all()
    return success_response([CommentResponse.model_validate(c).model_dump() for c in comments])


@router.put("/{comment_id}", response_model=dict)
def update_comment(
    comment_id: int,
    data: CommentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a comment (author only)."""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    comment.content = data.content
    db.commit()
    return success_response(message="Comment updated")


@router.delete("/{comment_id}", response_model=dict)
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a comment (author or admin)."""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id and current_user.role.value not in ["municipal_admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(comment)
    db.commit()
    return success_response(message="Comment deleted")
