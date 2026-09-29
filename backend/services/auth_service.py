"""Authentication service: JWT, password hashing, user management."""
from datetime import timedelta
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.user import User, OAuthAccount
from backend.schemas.auth import UserCreate, UserUpdate, UserRead, TokenData
from backend.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_oauth(self, provider: str, provider_user_id: str) -> Optional[User]:
        """Get user by OAuth provider and provider user ID."""
        result = await self.db.execute(
            select(User)
            .join(OAuthAccount)
            .where(
                OAuthAccount.provider == provider,
                OAuthAccount.provider_user_id == provider_user_id,
            )
            .options(selectinload(User.oauth_accounts))
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user with hashed password."""
        hashed_password = hash_password(user_data.password)
        user = User(
            email=user_data.email,
            name=user_data.name,
            avatar_url=user_data.avatar_url,
            hashed_password=hashed_password,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def create_oauth_user(
        self,
        email: str,
        name: str,
        provider: str,
        provider_user_id: str,
        avatar_url: Optional[str] = None,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        expires_at: Optional[int] = None,
    ) -> User:
        """Create a new user from OAuth."""
        user = User(
            email=email,
            name=name,
            avatar_url=avatar_url,
            hashed_password=None,  # OAuth users don't have passwords initially
        )
        self.db.add(user)
        await self.db.flush()  # Get user ID

        oauth_account = OAuthAccount(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
        )
        self.db.add(oauth_account)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def link_oauth_account(
        self,
        user: User,
        provider: str,
        provider_user_id: str,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        expires_at: Optional[int] = None,
    ) -> OAuthAccount:
        """Link an OAuth account to an existing user."""
        oauth_account = OAuthAccount(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
        )
        self.db.add(oauth_account)
        await self.db.commit()
        await self.db.refresh(oauth_account)
        return oauth_account

    async def update_user(self, user: User, user_data: UserUpdate) -> User:
        """Update user fields."""
        if user_data.name is not None:
            user.name = user_data.name
        if user_data.avatar_url is not None:
            user.avatar_url = user_data.avatar_url
        if user_data.is_active is not None:
            user.is_active = user_data.is_active
        if user_data.is_admin is not None:
            user.is_admin = user_data.is_admin

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def set_password(self, user: User, password: str) -> User:
        """Set or update user password."""
        user.hashed_password = hash_password(password)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not user.hashed_password:
            return None  # OAuth-only user
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user

    def create_token(self, user: User) -> str:
        """Create access token for user."""
        return create_access_token(
            subject=str(user.id),
            email=user.email,
            is_admin=user.is_admin,
        )

    def decode_token(self, token: str) -> Optional[TokenData]:
        """Decode token and return token data."""
        payload = decode_token(token)
        if not payload:
            return None

        return TokenData(
            sub=payload.get("sub", ""),
            email=payload.get("email", ""),
            is_admin=payload.get("is_admin", False),
            exp=payload.get("exp", 0),
        )

    async def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from token."""
        token_data = self.decode_token(token)
        if not token_data:
            return None

        user = await self.get_user_by_id(int(token_data.sub))
        if not user or not user.is_active:
            return None
        return user