"""
CivicResolve FastAPI application factory.
Registers all routers, middleware, and startup events.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import os

from backend.middleware.cors_middleware import add_cors
from backend.middleware.rate_limiter import limiter

# Route imports
from backend.routes.auth_routes import router as auth_router
from backend.routes.issue_routes import router as issue_router
from backend.routes.vote_routes import router as vote_router
from backend.routes.resolution_routes import router as resolution_router
from backend.routes.comment_routes import router as comment_router
from backend.routes.notification_routes import router as notification_router
from backend.routes.dashboard_routes import router as dashboard_router
from backend.routes.analytics_routes import router as analytics_router
from backend.routes.gamification_routes import router as gamification_router
from backend.routes.map_routes import router as map_router
from backend.routes.admin_routes import router as admin_router
from backend.routes.budget_routes import router as budget_router
from backend.routes.super_admin_routes import router as super_admin_router
from backend.routes.upload_routes import router as upload_router
from backend.routes.chatbot_routes import router as chatbot_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup."""
    from database.connection import init_db
    init_db()
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title="CivicResolve API",
        description=(
            "SIH 25031: Crowdsourced Civic Issue Reporting & Resolution System\n"
            "Government of Jharkhand | Clean & Green Technology Theme"
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Middleware
    add_cors(app)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Static file serving for uploaded media
    os.makedirs("uploads", exist_ok=True)
    app.mount("/static/uploads", StaticFiles(directory="uploads"), name="uploads")

    # Register all routers under /api/v1
    api_prefix = "/api/v1"
    for router in [
        auth_router, issue_router, vote_router, resolution_router,
        comment_router, notification_router, dashboard_router,
        analytics_router, gamification_router, map_router,
        admin_router, budget_router, super_admin_router,
        upload_router, chatbot_router,
    ]:
        app.include_router(router, prefix=api_prefix)

    @app.get("/", tags=["Root"])
    def root():
        """API root — health check."""
        return {
            "name": "CivicResolve API",
            "version": "1.0.0",
            "status": "running",
            "docs": "/docs",
        }

    return app
