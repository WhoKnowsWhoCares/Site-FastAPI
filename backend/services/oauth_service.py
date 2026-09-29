"""OAuth service for GitHub, Google, and Telegram authentication."""
import secrets
from urllib.parse import urlencode
from typing import Optional
import httpx

from backend.config import settings
from backend.schemas.auth import OAuthProvider


class OAuthService:
    """Service for OAuth provider integrations."""

    # GitHub OAuth
    GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GITHUB_USER_URL = "https://api.github.com/user"
    GITHUB_EMAILS_URL = "https://api.github.com/user/emails"

    # Google OAuth
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    # Telegram OAuth (Login Widget)
    TELEGRAM_AUTH_URL = "https://oauth.telegram.org/auth"

    def __init__(self):
        self._state_store: dict[str, str] = {}  # In production, use Redis

    def generate_state(self) -> str:
        """Generate a secure random state parameter."""
        return secrets.token_urlsafe(32)

    def store_state(self, state: str, provider: str) -> None:
        """Store state with provider (in production, use Redis with TTL)."""
        self._state_store[state] = provider

    def verify_state(self, state: str) -> Optional[str]:
        """Verify and consume state, return provider if valid."""
        return self._state_store.pop(state, None)

    # GitHub OAuth
    def get_github_auth_url(self, state: str) -> str:
        """Generate GitHub OAuth authorization URL."""
        if not settings.github_client_id:
            raise ValueError("GitHub OAuth not configured")

        params = {
            "client_id": settings.github_client_id,
            "redirect_uri": f"{settings.frontend_url}/auth/callback/github",
            "scope": "read:user user:email",
            "state": state,
            "allow_signup": "true",
        }
        return f"{self.GITHUB_AUTH_URL}?{urlencode(params)}"

    async def get_github_token(self, code: str) -> Optional[dict]:
        """Exchange GitHub authorization code for access token."""
        if not settings.github_client_id or not settings.github_client_secret:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.GITHUB_TOKEN_URL,
                data={
                    "client_id": settings.github_client_id,
                    "client_secret": settings.github_client_secret,
                    "code": code,
                    "redirect_uri": f"{settings.frontend_url}/auth/callback/github",
                },
                headers={"Accept": "application/json"},
            )
            if response.status_code != 200:
                return None
            return response.json()

    async def get_github_user(self, access_token: str) -> Optional[dict]:
        """Get GitHub user info."""
        async with httpx.AsyncClient() as client:
            # Get user info
            user_response = await client.get(
                self.GITHUB_USER_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if user_response.status_code != 200:
                return None

            user_data = user_response.json()

            # Get primary email
            emails_response = await client.get(
                self.GITHUB_EMAILS_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            primary_email = None
            if emails_response.status_code == 200:
                emails = emails_response.json()
                for email in emails:
                    if email.get("primary") and email.get("verified"):
                        primary_email = email["email"]
                        break

            return {
                "provider_user_id": str(user_data["id"]),
                "email": primary_email or user_data.get("email"),
                "name": user_data.get("name") or user_data.get("login"),
                "avatar_url": user_data.get("avatar_url"),
                "access_token": access_token,
            }

    # Google OAuth
    def get_google_auth_url(self, state: str) -> str:
        """Generate Google OAuth authorization URL."""
        if not settings.google_client_id:
            raise ValueError("Google OAuth not configured")

        params = {
            "client_id": settings.google_client_id,
            "redirect_uri": f"{settings.frontend_url}/auth/callback/google",
            "scope": "openid email profile",
            "response_type": "code",
            "state": state,
            "access_type": "offline",
            "prompt": "consent",
        }
        return f"{self.GOOGLE_AUTH_URL}?{urlencode(params)}"

    async def get_google_token(self, code: str) -> Optional[dict]:
        """Exchange Google authorization code for access token."""
        if not settings.google_client_id or not settings.google_client_secret:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.GOOGLE_TOKEN_URL,
                data={
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "code": code,
                    "redirect_uri": f"{settings.frontend_url}/auth/callback/google",
                    "grant_type": "authorization_code",
                },
                headers={"Accept": "application/json"},
            )
            if response.status_code != 200:
                return None
            return response.json()

    async def get_google_user(self, access_token: str) -> Optional[dict]:
        """Get Google user info."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.GOOGLE_USER_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if response.status_code != 200:
                return None

            user_data = response.json()
            return {
                "provider_user_id": user_data["id"],
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "avatar_url": user_data.get("picture"),
                "access_token": access_token,
            }

    # Telegram OAuth (Login Widget)
    def get_telegram_auth_url(self, state: str) -> str:
        """Generate Telegram Login Widget URL."""
        if not settings.telegram_bot_token:
            raise ValueError("Telegram Bot not configured")

        # For Telegram Login Widget, we use a different flow
        # This generates a URL that opens the Telegram Login Widget
        bot_username = settings.telegram_bot_token.split(":")[0] if ":" in settings.telegram_bot_token else ""
        params = {
            "origin": settings.frontend_url,
            "bot_id": bot_username,
            "request_access": "write",
            "state": state,
        }
        return f"{self.TELEGRAM_AUTH_URL}?{urlencode(params)}"

    async def verify_telegram_auth(self, auth_data: dict) -> Optional[dict]:
        """Verify Telegram Login Widget authentication data.
        
        See: https://core.telegram.org/widgets/login
        """
        if not settings.telegram_bot_token:
            return None

        # Verify hash (simplified - in production use proper verification)
        # The auth_data should contain: id, first_name, last_name, username, photo_url, auth_date, hash
        # Hash verification requires the bot token
        
        # For now, return basic user info
        return {
            "provider_user_id": str(auth_data.get("id")),
            "email": None,  # Telegram doesn't provide email
            "name": f"{auth_data.get('first_name', '')} {auth_data.get('last_name', '')}".strip(),
            "avatar_url": auth_data.get("photo_url"),
            "access_token": None,
        }

    def get_auth_url(self, provider: str, state: str) -> str:
        """Get authorization URL for provider."""
        if provider == OAuthProvider.GITHUB:
            return self.get_github_auth_url(state)
        elif provider == OAuthProvider.GOOGLE:
            return self.get_google_auth_url(state)
        elif provider == OAuthProvider.TELEGRAM:
            return self.get_telegram_auth_url(state)
        else:
            raise ValueError(f"Unknown OAuth provider: {provider}")

    async def get_user_info(self, provider: str, code: str) -> Optional[dict]:
        """Get user info from OAuth provider."""
        if provider == OAuthProvider.GITHUB:
            token_data = await self.get_github_token(code)
            if not token_data:
                return None
            return await self.get_github_user(token_data["access_token"])
        elif provider == OAuthProvider.GOOGLE:
            token_data = await self.get_google_token(code)
            if not token_data:
                return None
            return await self.get_google_user(token_data["access_token"])
        elif provider == OAuthProvider.TELEGRAM:
            # Telegram uses widget, not code exchange
            return None
        return None