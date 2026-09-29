"""OAuth provider registry and flows: GitHub, Google, Telegram."""
import hashlib
import hmac
import secrets
from dataclasses import dataclass, field
from typing import Any

import httpx
from fastapi import HTTPException, status

from backend.config import settings


@dataclass
class OAuthProvider:
    name: str
    authorize_url: str | None
    token_url: str | None
    client_id: str | None
    client_secret: str | None
    scopes: list[str] = field(default_factory=list)
    extra_params: dict[str, str] = field(default_factory=dict)


def _build_providers() -> dict[str, OAuthProvider]:
    return {
        "github": OAuthProvider(
            name="github",
            authorize_url="https://github.com/login/oauth/authorize",
            token_url="https://github.com/login/oauth/access_token",
            client_id=settings.GITHUB_CLIENT_ID,
            client_secret=settings.GITHUB_CLIENT_SECRET,
            scopes=["read:user", "user:email"],
        ),
        "google": OAuthProvider(
            name="google",
            authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
            token_url="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=["openid", "email", "profile"],
        ),
        "telegram": OAuthProvider(
            name="telegram",
            authorize_url="https://oauth.telegram.org/auth",
            token_url=None,  # Telegram Login Widget: identity comes signed from the widget
            client_id=str(settings.TELEGRAM_BOT_ID) if settings.TELEGRAM_BOT_ID else None,
            client_secret=settings.TELEGRAM_BOT_TOKEN,
            extra_params={"bot_id": settings.TELEGRAM_BOT_ID or ""},
        ),
    }


PROVIDERS: dict[str, OAuthProvider] = _build_providers()


def get_provider(name: str) -> OAuthProvider:
    provider = PROVIDERS.get(name)
    if provider is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown OAuth provider: {name}",
        )
    return provider


def _redirect_uri(provider_name: str) -> str:
    return f"{settings.FRONTEND_URL.rstrip('/')}/api/v1/auth/callback/{provider_name}"


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def build_oauth_url(provider: str | OAuthProvider, state: str) -> str:
    from urllib.parse import urlencode

    p: OAuthProvider = provider if isinstance(provider, OAuthProvider) else get_provider(provider)
    if p.name == "telegram":
        params = {"bot_id": p.extra_params["bot_id"], "state": state}
        return f"{p.authorize_url}?{urlencode(params)}"

    params = {
        "client_id": p.client_id or "",
        "redirect_uri": _redirect_uri(p.name),
        "state": state,
        "response_type": "code",
        "scope": " ".join(p.scopes),
    }
    return f"{p.authorize_url}?{urlencode(params)}"


def verify_telegram_auth(data: dict[str, Any]) -> bool:
    """Verify Telegram Login Widget signature (HMAC-SHA256 with bot token)."""
    check_hash = data.pop("hash", None)
    if not check_hash:
        return False
    secret = hashlib.sha256((settings.TELEGRAM_BOT_TOKEN or "").encode()).digest()
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    computed = hmac.new(secret, data_check_string.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, check_hash)


async def exchange_code(provider: OAuthProvider, code: str) -> dict[str, Any]:
    """Exchange OAuth authorization code for provider identity info.

    Returns a dict with at least: provider, provider_account_id, email, name.
    """
    if provider.name == "telegram":
        # Telegram widget flow: the "code" is JSON auth data from the widget.
        import json

        try:
            data = json.loads(code)
        except json.JSONDecodeError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid Telegram auth data")
        if not verify_telegram_auth(data):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid Telegram signature")
        return {
            "provider": "telegram",
            "provider_account_id": str(data["id"]),
            "email": data.get("email", f"tg{data['id']}@telegram.local"),
            "name": data.get("first_name", data.get("username", "Telegram User")),
        }

    if not provider.client_id or not provider.client_secret:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"OAuth provider '{provider.name}' is not configured",
        )

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            provider.token_url,
            data={
                "client_id": provider.client_id,
                "client_secret": provider.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": _redirect_uri(provider.name),
            },
            headers={"Accept": "application/json"},
        )
        if token_resp.status_code != 200:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="OAuth code exchange failed")
        access_token = token_resp.json().get("access_token")

        if provider.name == "github":
            user_resp = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            gh = user_resp.json()
            email = gh.get("email")
            if not email:
                emails_resp = await client.get(
                    "https://api.github.com/user/emails",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                for e in emails_resp.json() or []:
                    if e.get("primary"):
                        email = e["email"]
                        break
            return {
                "provider": "github",
                "provider_account_id": str(gh["id"]),
                "email": email or f"gh{gh['id']}@users.noreply.github.com",
                "name": gh.get("name") or gh.get("login", "GitHub User"),
            }
        else:  # google
            info_resp = await client.get(
                "https://openidconnect.googleapis.com/v1/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            info = info_resp.json()
            return {
                "provider": "google",
                "provider_account_id": info["sub"],
                "email": info.get("email"),
                "name": info.get("name", "Google User"),
            }
