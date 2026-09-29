"""Unit tests for oauth_service: OAuth URL generation for GitHub, Google, Telegram."""
import pytest
from fastapi import HTTPException

from backend.services.oauth_service import (
    PROVIDERS,
    build_oauth_url,
    exchange_code,
    get_provider,
)


class TestProviderRegistry:
    def test_all_three_providers_registered(self):
        assert set(PROVIDERS) == {"github", "google", "telegram"}

    def test_get_provider_unknown_raises(self):
        with pytest.raises(HTTPException) as exc:
            get_provider("facebook")
        assert exc.value.status_code == 404

    def test_get_provider_known(self):
        assert get_provider("github").name == "github"


class TestBuildOauthUrl:
    def test_github_authorize_url(self):
        url = build_oauth_url("github", state="st-123")
        assert url.startswith("https://github.com/login/oauth/authorize")
        assert "client_id=" in url
        assert "state=st-123" in url

    def test_google_authorize_url(self):
        url = build_oauth_url("google", state="st-456")
        assert url.startswith("https://accounts.google.com/o/oauth2/v2/auth")
        assert "scope=" in url
        assert "response_type=code" in url
        assert "redirect_uri=" in url

    def test_telegram_login_url(self):
        url = build_oauth_url("telegram", state="st-789")
        assert "oauth.telegram.org" in url or "t.me" in url
        assert "bot_id=" in url

    def test_unknown_provider_rejected(self):
        with pytest.raises(HTTPException):
            build_oauth_url("facebook", state="x")


class TestExchangeCode:
    async def test_exchange_missing_credentials_returns_501(self):
        # No client secret configured -> cannot exchange -> 501
        import backend.services.oauth_service as svc

        provider = svc.get_provider("github")
        saved = provider.client_secret
        provider.client_secret = None
        try:
            with pytest.raises(HTTPException) as exc:
                await svc.exchange_code(provider, "code")
            assert exc.value.status_code == 501
        finally:
            provider.client_secret = saved

    async def test_telegram_widget_flow_exchanges_hash_not_http(self):
        # Telegram uses widget auth data (signed JSON), not an HTTP code exchange
        import hashlib
        import hmac
        import json

        import backend.services.oauth_service as svc
        from backend.config import settings

        bot_token = settings.TELEGRAM_BOT_TOKEN or "12345:testtoken"
        auth_data = {"id": 777000, "first_name": "Alexander", "auth_date": "1700000000"}
        secret = hashlib.sha256(bot_token.encode()).digest()
        check_string = "\n".join(f"{k}={v}" for k, v in sorted(auth_data.items()))
        auth_data["hash"] = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()

        provider = svc.get_provider("telegram")
        saved = settings.TELEGRAM_BOT_TOKEN
        settings.TELEGRAM_BOT_TOKEN = bot_token
        try:
            result = await svc.exchange_code(provider, json.dumps(auth_data))
        finally:
            settings.TELEGRAM_BOT_TOKEN = saved
        assert result["provider"] == "telegram"
        assert result["provider_account_id"] == "777000"
