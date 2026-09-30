"""Schemas package exports."""
from backend.schemas.auth import (
    AuthMessage,
    OAuthCallback,
    OAuthProvider,
    OAuthUrlResponse,
    Token,
    TokenData,
    UserBase,
    UserCreate,
    UserRead,
    UserUpdate,
)
from backend.schemas.common import (
    ErrorResponse,
    HealthCheckResponse,
    PaginatedResponse,
    PaginationParams,
    SuccessResponse,
)
from backend.schemas.content import (
    ContentBase,
    ContentCreate,
    ContentList,
    ContentRead,
    ContentType,
    ContentUpdate,
    MediaBase,
    MediaRead,
    ProjectBase,
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
    SectionType,
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
