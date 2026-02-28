"""File upload and storage utilities."""

import logging
import os
import uuid
from typing import Optional
from fastapi import UploadFile

logger = logging.getLogger(__name__)


def generate_unique_filename(original_filename: str) -> str:
    """Generate a UUID-based unique filename preserving extension."""
    ext = os.path.splitext(original_filename)[1].lower()
    return f"{uuid.uuid4().hex}{ext}"


def get_file_size_mb(file: UploadFile) -> float:
    """Get file size in megabytes."""
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    return size / (1024 * 1024)


def upload_to_cloudinary(file_path: str, folder: str = "civicresolve") -> Optional[str]:
    """Upload a file to Cloudinary and return the public URL."""
    try:
        import cloudinary
        import cloudinary.uploader
        from config.settings import settings

        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
        )
        result = cloudinary.uploader.upload(file_path, folder=folder)
        return result.get("secure_url")
    except Exception as e:
        logger.error("Cloudinary upload failed: %s", e)
        return None


def save_file_locally(file: UploadFile, directory: str = "uploads") -> str:
    """Save an uploaded file locally and return the path."""
    os.makedirs(directory, exist_ok=True)
    filename = generate_unique_filename(file.filename or "upload")
    filepath = os.path.join(directory, filename)
    with open(filepath, "wb") as f:
        content = file.file.read()
        f.write(content)
    return filepath
