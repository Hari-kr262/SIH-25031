"""Authentication service — register, login, token management."""

from datetime import timedelta
from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.models.user import User
from backend.schemas.auth import LoginRequest, TokenResponse
from backend.schemas.user import UserCreate
from backend.utils.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token, generate_otp
)
from backend.utils.time_utils import now_utc
from backend.services.audit_service import log_action


# In-memory OTP store (use Redis in production)
_otp_store: Dict[str, Dict[str, Any]] = {}


class AuthService:
    """Handles all authentication-related operations."""

    def register(self, db: Session, user_data: UserCreate) -> User:
        """Register a new user."""
        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hash_password(user_data.password),
            role=user_data.role,
            preferred_language=user_data.preferred_language,
            is_active=True,
            is_verified=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        log_action(db, user.id, "user.register", "user", user.id)
        return user

    def login(self, db: Session, credentials: LoginRequest, ip_address: str = "") -> TokenResponse:
        """Authenticate user and return JWT tokens."""
        user = db.query(User).filter(
            User.email == credentials.email,
            User.is_active == True
        ).first()

        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Update last login
        user.last_login_at = now_utc()
        db.commit()

        token_data = {"sub": str(user.id), "role": user.role.value, "email": user.email}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        log_action(db, user.id, "user.login", "user", user.id, ip_address=ip_address)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            role=user.role.value,
            full_name=user.full_name,
        )

    def refresh_tokens(self, db: Session, refresh_token: str) -> TokenResponse:
        """Generate new access + refresh tokens from a valid refresh token."""
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == int(user_id), User.is_active == True).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        token_data = {"sub": str(user.id), "role": user.role.value, "email": user.email}
        return TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
            user_id=user.id,
            role=user.role.value,
            full_name=user.full_name,
        )

    def send_otp(self, db: Session, email: str) -> bool:
        """Generate and store OTP for email verification."""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False  # Don't leak whether email exists
        otp = generate_otp()
        _otp_store[email] = {
            "otp": otp,
            "expires_at": now_utc() + timedelta(minutes=10),
        }
        # TODO: Send OTP via email using notification_service
        print(f"[DEV] OTP for {email}: {otp}")
        return True

    def verify_otp(self, db: Session, email: str, otp: str) -> bool:
        """Verify OTP and mark user as verified."""
        stored = _otp_store.get(email)
        if not stored:
            return False
        if now_utc() > stored["expires_at"]:
            del _otp_store[email]
            return False
        if stored["otp"] != otp:
            return False
        del _otp_store[email]
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.is_verified = True
            db.commit()
        return True

    def forgot_password(self, db: Session, email: str) -> bool:
        """Send a password reset OTP."""
        return self.send_otp(db, email)

    def reset_password(self, db: Session, email: str, otp: str, new_password: str) -> bool:
        """Reset password after OTP verification."""
        if not self.verify_otp(db, email, otp):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP",
            )
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False
        user.password_hash = hash_password(new_password)
        db.commit()
        log_action(db, user.id, "user.password_reset", "user", user.id)
        return True


auth_service = AuthService()
