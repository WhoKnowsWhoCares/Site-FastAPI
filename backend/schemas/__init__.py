"""Schemas package exports."""
from backend.schemas.auth import (
    Token,
    TokenData,
    UserBase,
    UserCreate,
    UserUpdate,
    UserRead,
    OAuthUrlResponse,
    OAuthCallback,
    OAuthProvider,
    AuthMessage,
)
from backend.schemas.content import (
    SectionType,
    ContentType,
    ContentBase,
    ContentCreate,
    ContentUpdate,
    ContentRead,
    ContentList,
    ProjectBase,
    ProjectCreate,
    ProjectUpdate,
    ProjectRead,
    MediaBase,
    MediaRead,
)
from backend.schemas.common import (
    PaginationParams,
    PaginatedResponse,
    ErrorResponse,
    SuccessResponse,
    HealthCheckResponse,
)

__all__ = [
    # auth
    "Token",
    "TokenData",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserRead",
    "OAuthUrlResponse",
    "OAuthCallback",
    "OAuthProvider",
    "AuthMessage",
    # content
    "SectionType",
    "ContentType",
    "ContentBase",
    "ContentCreate",
    "ContentUpdate",
    "ContentRead",
    "ContentList",
    "ProjectBase",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectRead",
    "MediaBase",
    "MediaRead",
    # common
    "PaginationParams",
    "PaginatedResponse",
    "ErrorResponse",
    "SuccessResponse",
    "HealthCheckResponse",
]