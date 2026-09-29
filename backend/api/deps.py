"""API dependencies."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.user import User
from backend.schemas.auth import OAuthProvider
from backend.services.auth_service import AuthService
from backend.services.oauth_service import OAuthService


# Security scheme
security = HTTPBearer()


async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """Dependency for getting AuthService."""
    return AuthService(db)


async def get_oauth_service() -> OAuthService:
    """Dependency for getting OAuthService."""
    return OAuthService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """Get current authenticated user from bearer token."""
    token = credentials.credentials

    user = await auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_admin(
    current_user=Depends(get_current_user),
) -> dict:
    """Get current admin user. Requires is_admin=True."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "is_admin": True,
    }


async def get_provider(provider: str) -> str:
    """Validate OAuth provider."""
    valid_providers = ["github", "google", "telegram"]
    if provider not in valid_providers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid OAuth provider. Valid providers: {valid_providers}",
        )
    return provider