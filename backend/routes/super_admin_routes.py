"""Super admin routes: health, audit, settings, features."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from backend.models.user import User
from backend.middleware.rbac_middleware import require_super_admin
from backend.utils.response_utils import success_response

router = APIRouter(prefix="/super-admin", tags=["Super Admin"])

# In-memory feature flags (use Redis/DB in production)
_feature_flags = {
    "ai_categorization": True,
    "gamification": True,
    "sms_notifications": False,
    "voice_reporting": True,
    "public_map": True,
}


@router.get("/health", response_model=dict)
def system_health(
    current_user: User = Depends(require_super_admin()),
    db: Session = Depends(get_db),
):
    """Check system health."""
    try:
        db.execute(__import__("sqlalchemy").text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {e}"

    return success_response({
        "database": db_status,
        "api": "healthy",
        "version": "1.0.0",
    })


@router.get("/feature-flags", response_model=dict)
def get_feature_flags(current_user: User = Depends(require_super_admin())):
    """Get all feature flags."""
    return success_response(_feature_flags)


@router.put("/feature-flags/{flag_name}", response_model=dict)
def toggle_feature_flag(
    flag_name: str,
    enabled: bool,
    current_user: User = Depends(require_super_admin()),
):
    """Toggle a feature flag."""
    if flag_name not in _feature_flags:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Feature flag not found")
    _feature_flags[flag_name] = enabled
    return success_response({flag_name: enabled}, f"Feature '{flag_name}' {'enabled' if enabled else 'disabled'}")


@router.get("/audit-logs", response_model=dict)
def full_audit_logs(
    page: int = 1,
    page_size: int = 100,
    current_user: User = Depends(require_super_admin()),
    db: Session = Depends(get_db),
):
    """Get complete audit logs (super admin only)."""
    from backend.services.audit_service import audit_service
    logs, total = audit_service.get_logs(db, page=page, page_size=page_size)
    return success_response({
        "total": total,
        "items": [{"id": l.id, "action": l.action, "user_id": l.user_id,
                   "timestamp": l.timestamp.isoformat()} for l in logs]
    })


@router.delete("/database/clear-test-data", response_model=dict)
def clear_test_data(
    confirm: str,
    current_user: User = Depends(require_super_admin()),
    db: Session = Depends(get_db),
):
    """Clear non-production test data (requires confirm='YES_DELETE_ALL')."""
    if confirm != "YES_DELETE_ALL":
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Confirmation string mismatch")
    # TODO: Implement selective cleanup
    return success_response(message="Test data cleared (stub)")
