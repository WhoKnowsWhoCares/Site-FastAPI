"""Authentication endpoints: OAuth, login, logout."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_provider, get_current_user, get_auth_service, get_oauth_service
from backend.database import get_db
from backend.schemas.auth import (
    Token,
    OAuthUrlResponse,
    OAuthCallback,
    AuthMessage,
    UserRead,
)
from backend.schemas.content import SectionType
from backend.services.auth_service import AuthService
from backend.services.oauth_service import OAuthService


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.get("/oauth/{provider}/url")
async def get_oauth_url(
    provider: str,
    oauth_service: OAuthService = Depends(get_oauth_service),
):
    """Get OAuth authorization URL for a provider."""
    provider = await get_provider(provider)
    state = oauth_service.generate_state()
    oauth_service.store_state(state, provider)

    auth_url = oauth_service.get_auth_url(provider, state)
    return OAuthUrlResponse(authorization_url=auth_url, state=state)


@router.post("/oauth/{provider}/callback")
async def oauth_callback(
    callback_data: OAuthCallback,
    provider: str,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
    oauth_service: OAuthService = Depends(get_oauth_service),
):
    """Handle OAuth callback from provider."""
    if callback_data.error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth error: {callback_data.error}",
        )

    provider = await get_provider(provider)

    # Verify state
    stored_provider = oauth_service.verify_state(callback_data.state)
    if not stored_provider or stored_provider != provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OAuth state",
        )

    # Get user info from provider
    user_info = await oauth_service.get_user_info(provider, callback_data.code)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get user info from OAuth provider",
        )

    # Find or create user
    existing_user = await auth_service.get_user_by_oauth(
        provider, user_info["provider_user_id"]
    )

    if existing_user:
        # Link OAuth account if not linked
        user = existing_user
    else:
        # Create new user from OAuth
        user = await auth_service.create_oauth_user(
            email=user_info["email"],
            name=user_info["name"],
            avatar_url=user_info.get("avatar_url"),
            provider=provider,
            provider_user_id=user_info["provider_user_id"],
            access_token=user_info.get("access_token"),
        )

    # Create token
    token = auth_service.create_token(user)

    return Token(access_token=token, expires_in=1800)


@router.post("/oauth/{provider}/telegram/callback")
async def telegram_callback(
    callback_data: OAuthCallback,
    provider: str,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
    oauth_service: OAuthService = Depends(get_oauth_service),
):
    """Handle Telegram Login Widget callback."""
    if callback_data.error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Telegram error: {callback_data.error}",
        )

    provider = await get_provider(provider)

    # Verify state
    stored_provider = oauth_service.verify_state(callback_data.state)
    if not stored_provider or stored_provider != provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Telegram state",
        )

    # Verify Telegram auth data
    user_info = await oauth_service.verify_telegram_auth(callback_data.model_dump())
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to verify Telegram authentication",
        )

    # Find or create user
    existing_user = await auth_service.get_user_by_oauth(
        provider, user_info["provider_user_id"]
    )

    if existing_user:
        user = existing_user
    else:
        user = await auth_service.create_oauth_user(
            email=None,  # Telegram doesn't provide email
            name=user_info["name"],
            avatar_url=user_info.get("avatar_url"),
            provider=provider,
            provider_user_id=user_info["provider_user_id"],
        )

    token = auth_service.create_token(user)
    return Token(access_token=token, expires_in=1800)


@router.post("/login")
async def login(
    callback_data: OAuthCallback,  # Using email as code field for simplicity
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Login with email and password (using OAuthCallback structure)."""
    # This is a placeholder - in production use proper login form
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Email/password login not yet implemented",
    )


@router.get("/me")
async def get_me(
    current_user: dict = Depends(get_current_user),
):
    """Get current user info."""
    return UserRead(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        avatar_url=current_user.avatar_url,
        is_active=current_user.is_active,
        is_admin=current_user.is_admin,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.post("/logout")
async def logout(
    message: AuthMessage = AuthMessage(message="Logged out successfully"),
):
    """Logout endpoint (stateless - token invalidation handled client-side)."""
    return message


@router.get("/sections")
async def get_available_sections():
    """Get available content sections."""
    return [s.value for s in SectionType]