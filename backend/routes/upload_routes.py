"""Upload routes: image, video, document uploads."""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from backend.models.user import User
from backend.middleware.auth_middleware import get_current_user
from backend.utils.file_utils import get_file_size_mb, save_file_locally
from backend.utils.response_utils import success_response
from config.constants import (
    MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB,
    ALLOWED_IMAGE_TYPES, ALLOWED_VIDEO_TYPES
)

router = APIRouter(prefix="/uploads", tags=["Uploads"])


@router.post("/image", response_model=dict)
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Upload an image file. Returns the file URL."""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image type")
    size_mb = get_file_size_mb(file)
    if size_mb > MAX_IMAGE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"Image too large (max {MAX_IMAGE_SIZE_MB}MB)")

    filepath = save_file_locally(file, directory="uploads/images")
    # TODO: Upload to Cloudinary and return CDN URL
    return success_response({"url": f"/static/{filepath}", "size_mb": round(size_mb, 2)})


@router.post("/video", response_model=dict)
async def upload_video(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Upload a video file. Returns the file URL."""
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=400, detail="Invalid video type")
    size_mb = get_file_size_mb(file)
    if size_mb > MAX_VIDEO_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"Video too large (max {MAX_VIDEO_SIZE_MB}MB)")

    filepath = save_file_locally(file, directory="uploads/videos")
    return success_response({"url": f"/static/{filepath}", "size_mb": round(size_mb, 2)})


@router.post("/document", response_model=dict)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Upload a document (PDF, Word). Returns the file URL."""
    from config.constants import ALLOWED_DOCUMENT_TYPES
    if file.content_type not in ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid document type")
    filepath = save_file_locally(file, directory="uploads/documents")
    return success_response({"url": f"/static/{filepath}"})
