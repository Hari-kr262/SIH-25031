"""Resolution routes: submit proof, verify, compare, rate."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.user import User
from backend.schemas.resolution import ResolutionCreate, ResolutionVerify, ResolutionResponse
from backend.services.resolution_service import resolution_service
from backend.middleware.auth_middleware import get_current_user
from backend.utils.response_utils import success_response

router = APIRouter(prefix="/resolutions", tags=["Resolutions"])


@router.post("/", response_model=dict, status_code=201)
def submit_proof(
    data: ResolutionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Field worker submits proof of fix."""
    resolution = resolution_service.submit_proof(db, data, current_user.id)
    return success_response({"resolution_id": resolution.id}, "Proof submitted successfully")


@router.get("/{issue_id}", response_model=ResolutionResponse)
def get_resolution(issue_id: int, db: Session = Depends(get_db)):
    """Get resolution for an issue."""
    from backend.models.resolution import Resolution
    from fastapi import HTTPException
    res = db.query(Resolution).filter_by(issue_id=issue_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="No resolution found for this issue")
    return res


@router.post("/{issue_id}/verify", response_model=dict)
def verify_resolution(
    issue_id: int,
    data: ResolutionVerify,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Citizen verifies whether the fix is satisfactory."""
    resolution = resolution_service.verify_resolution(db, issue_id, data, current_user.id)
    status_msg = "Resolution verified as satisfactory" if data.citizen_verified else "Resolution marked as unsatisfactory"
    return success_response({"resolution_id": resolution.id}, status_msg)


@router.post("/{issue_id}/rate", response_model=dict)
def rate_resolution(
    issue_id: int,
    rating: int,
    feedback: str = "",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Rate a resolution 1-5 stars."""
    from backend.models.resolution import Resolution
    res = db.query(Resolution).filter_by(issue_id=issue_id).first()
    if not res:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Resolution not found")
    res.citizen_rating = max(1, min(5, rating))
    res.citizen_feedback = feedback
    db.commit()
    return success_response(message="Rating submitted")
