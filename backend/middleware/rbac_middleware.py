"""Role-Based Access Control (RBAC) helpers as FastAPI dependencies."""

from fastapi import HTTPException, status, Depends
from backend.models.user import User, UserRole
from backend.middleware.auth_middleware import get_current_user


def require_roles(*roles: UserRole):
    """Factory: return a dependency that enforces one of the given roles."""
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in roles]}",
            )
        return current_user
    return dependency


# Convenience role checkers
require_citizen = require_roles(
    UserRole.citizen, UserRole.volunteer, UserRole.field_worker,
    UserRole.department_head, UserRole.municipal_admin, UserRole.super_admin
)
require_volunteer = require_roles(
    UserRole.volunteer, UserRole.department_head, UserRole.municipal_admin, UserRole.super_admin
)
require_field_worker = require_roles(
    UserRole.field_worker, UserRole.department_head, UserRole.municipal_admin, UserRole.super_admin
)
require_department_head = require_roles(
    UserRole.department_head, UserRole.municipal_admin, UserRole.super_admin
)
require_admin = require_roles(UserRole.municipal_admin, UserRole.super_admin)
require_super_admin = require_roles(UserRole.super_admin)
