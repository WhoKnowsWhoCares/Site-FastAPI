"""Authentication schemas."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Token(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token payload data."""

    sub: str  # user id
    email: EmailStr
    is_admin: bool = False
    exp: int


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    avatar_url: str | None = None


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """User update schema."""

    name: str | None = Field(None, min_length=1, max_length=255)
    avatar_url: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = None


class UserRead(UserBase):
    """User read schema (public)."""

    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OAuthUrlResponse(BaseModel):
    """OAuth authorization URL response."""

    authorization_url: str
    state: str


class OAuthCallback(BaseModel):
    """OAuth callback parameters."""

    code: str
    state: str
    error: str | None = None
    error_description: str | None = None


class OAuthProvider(str):
    """OAuth provider names."""

    GITHUB = "github"
    GOOGLE = "google"
    TELEGRAM = "telegram"


class AuthMessage(BaseModel):
    """Auth-related message response."""

    message: str
