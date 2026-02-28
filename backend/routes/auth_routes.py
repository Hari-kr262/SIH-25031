"""Authentication routes: register, login, OTP, refresh, forgot/reset password, profile."""

from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db
from backend.schemas.auth import (
    LoginRequest, TokenResponse, RefreshRequest,
    ForgotPasswordRequest, OTPVerifyRequest
)
from backend.schemas.user import UserCreate, UserResponse, UserUpdate, PasswordChange
from backend.services.auth_service import auth_service
from backend.middleware.auth_middleware import get_current_user
from backend.models.user import User
from backend.utils.security import hash_password
from backend.utils.response_utils import success_response, error_response

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=dict, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new citizen account."""
    user = auth_service.register(db, user_data)
    return success_response({"id": user.id, "email": user.email}, "Registration successful")


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """Login with email and password."""
    ip = request.client.host if request.client else "unknown"
    return auth_service.login(db, credentials, ip_address=ip)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(data: RefreshRequest, db: Session = Depends(get_db)):
    """Refresh JWT access token using a refresh token."""
    return auth_service.refresh_tokens(db, data.refresh_token)


@router.post("/send-otp", response_model=dict)
def send_otp(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Send OTP to email for verification."""
    auth_service.send_otp(db, data.email)
    return success_response(message="OTP sent if email exists")


@router.post("/verify-otp", response_model=dict)
def verify_otp(data: OTPVerifyRequest, db: Session = Depends(get_db)):
    """Verify OTP for email verification."""
    verified = auth_service.verify_otp(db, data.email, data.otp)
    if not verified:
        return error_response("Invalid or expired OTP", 400)
    return success_response(message="Email verified successfully")


@router.post("/forgot-password", response_model=dict)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Send password reset OTP."""
    auth_service.forgot_password(db, data.email)
    return success_response(message="Password reset OTP sent if email exists")


@router.post("/reset-password-with-otp", response_model=dict)
def reset_password_with_otp(
    email: str, otp: str, new_password: str,
    db: Session = Depends(get_db)
):
    """Reset password with email + OTP."""
    auth_service.reset_password(db, email, otp, new_password)
    return success_response(message="Password reset successful")


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user profile."""
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/change-password", response_model=dict)
def change_password(
    data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change password for authenticated user."""
    from backend.utils.security import verify_password
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current_user.password_hash = hash_password(data.new_password)
    db.commit()
    return success_response(message="Password changed successfully")
