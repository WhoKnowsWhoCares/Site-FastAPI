"""Auth endpoints: OAuth initiation/callback, me, logout."""
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_current_user
from backend.database import get_db
from backend.models.user import OAuthAccount, User
from backend.schemas.auth import OAuthCallback, OAuthUrlResponse, Token, UserRead
from backend.services.auth_service import create_access_token
from backend.services.oauth_service import (
    build_oauth_url,
    exchange_code,
    generate_state,
    get_provider,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/oauth/{provider}", response_model=OAuthUrlResponse)
async def start_oauth(provider: str) -> OAuthUrlResponse:
    """Initiate an OAuth flow: return the provider's authorize URL + state."""
    p = get_provider(provider)
    state = generate_state()
    url = build_oauth_url(p, state)
    return OAuthUrlResponse(provider=p.name, url=url, state=state)


@router.post("/callback/{provider}", response_model=Token)
async def oauth_callback(
    provider: str,
    body: OAuthCallback,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """Handle the OAuth callback: exchange code, upsert user, issue JWT."""
    p = get_provider(provider)
    identity: dict[str, Any] = await exchange_code(p, body.code)

    result = await db.execute(
        select(User)
        .join(OAuthAccount)
        .where(
            OAuthAccount.provider == identity["provider"],
            OAuthAccount.provider_account_id == identity["provider_account_id"],
        )
    )
    user = result.scalar_one_or_none()

    if user is None:
        email_result = await db.execute(select(User).where(User.email == identity["email"]))
        user = email_result.scalar_one_or_none()
        if user is None:
            user = User(
                email=identity["email"],
                name=identity.get("name", ""),
                is_active=True,
            )
            db.add(user)
            await db.flush()
        db.add(
            OAuthAccount(
                user_id=user.id,
                provider=identity["provider"],
                provider_account_id=identity["provider_account_id"],
            )
        )
        await db.commit()

    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
async def read_me(user: User = Depends(get_current_user)) -> User:
    return user


@router.post("/logout")
async def logout() -> dict[str, str]:
    """Stateless JWT logout — client discards the token."""
    return {"detail": "Logged out"}
