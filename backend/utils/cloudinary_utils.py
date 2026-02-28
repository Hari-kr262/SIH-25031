"""Cloudinary upload utilities."""
import cloudinary
import cloudinary.uploader
from config.settings import settings


def configure_cloudinary():
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


def upload_to_cloudinary(file_bytes: bytes, folder: str = "civicresolve", resource_type: str = "image") -> dict:
    configure_cloudinary()
    result = cloudinary.uploader.upload(file_bytes, folder=folder, resource_type=resource_type)
    return {"url": result.get("secure_url"), "public_id": result.get("public_id")}
