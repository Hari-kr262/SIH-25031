"""CORS configuration helper."""

from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings


def add_cors(app):
    """Add CORS middleware to the FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )
