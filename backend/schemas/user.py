"""Pydantic schemas for User model."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from backend.models.user import UserRole


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: UserRole = UserRole.citizen
    preferred_language: str = "en"


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    preferred_language: Optional[str] = None
    assigned_area: Optional[str] = None


class UserResponse(UserBase):
    id: int
    avatar_url: Optional[str] = None
    department_id: Optional[int] = None
    is_trusted_volunteer: bool = False
    points: int = 0
    level: int = 1
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    """Public-facing user info (hides sensitive fields)."""
    id: int
    full_name: str
    avatar_url: Optional[str] = None
    role: UserRole
    points: int
    level: int

    model_config = ConfigDict(from_attributes=True)


class PasswordChange(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v
