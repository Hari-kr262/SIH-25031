"""Upload routes: image, video, document uploads."""

import logging

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from backend.models.user import User
from backend.middleware.auth_middleware import get_current_user
from backend.utils.file_utils import save_file_locally_from_bytes
from backend.utils.cloudinary_utils import upload_to_cloudinary
from backend.utils.response_utils import success_response
from config.constants import (
    MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB,
    ALLOWED_IMAGE_TYPES, ALLOWED_VIDEO_TYPES
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/uploads", tags=["Uploads"])


@router.post("/image", response_model=dict)
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Upload an image file. Returns the file URL."""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image type")
    file_bytes = await file.read()
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"Image too large (max {MAX_IMAGE_SIZE_MB}MB)")

    try:
        result = upload_to_cloudinary(file_bytes, folder="civicresolve/images", resource_type="image")
        url = result["url"]
    except Exception as e:
        logger.warning("Cloudinary upload failed, falling back to local storage: %s", e)
        filepath = save_file_locally_from_bytes(file_bytes, file.filename or "upload", directory="uploads/images")
        url = f"/static/{filepath}"

    return success_response({"url": url, "size_mb": round(size_mb, 2)})


@router.post("/video", response_model=dict)
async def upload_video(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Upload a video file. Returns the file URL."""
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=400, detail="Invalid video type")
    file_bytes = await file.read()
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_VIDEO_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"Video too large (max {MAX_VIDEO_SIZE_MB}MB)")

    try:
        result = upload_to_cloudinary(file_bytes, folder="civicresolve/videos", resource_type="video")
        url = result["url"]
    except Exception as e:
        logger.warning("Cloudinary upload failed, falling back to local storage: %s", e)
        filepath = save_file_locally_from_bytes(file_bytes, file.filename or "upload", directory="uploads/videos")
        url = f"/static/{filepath}"

    return success_response({"url": url, "size_mb": round(size_mb, 2)})


@router.post("/document", response_model=dict)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Upload a document (PDF, Word). Returns the file URL."""
    from config.constants import ALLOWED_DOCUMENT_TYPES
    if file.content_type not in ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid document type")
    file_bytes = await file.read()

    try:
        result = upload_to_cloudinary(file_bytes, folder="civicresolve/documents", resource_type="raw")
        url = result["url"]
    except Exception as e:
        logger.warning("Cloudinary upload failed, falling back to local storage: %s", e)
        filepath = save_file_locally_from_bytes(file_bytes, file.filename or "upload", directory="uploads/documents")
        url = f"/static/{filepath}"

    return success_response({"url": url})
