"""Integration tests for OAuth service methods."""
import pytest

from backend.services.oauth_service import OAuthService


@pytest.fixture
def oauth_service():
    """Create a fresh OAuthService instance for each test."""
    return OAuthService()


def test_generate_state(oauth_service: OAuthService):
    """Test state generation produces a non-empty string."""
    state = oauth_service.generate_state()
    assert isinstance(state, str)
    assert len(state) > 0


def test_store_and_verify_state(oauth_service: OAuthService):
    """Test storing and verifying OAuth state."""
    state = oauth_service.generate_state()
    oauth_service.store_state(state, "github")

    result = oauth_service.verify_state(state)
    assert result == "github"


def test_verify_state_consumes_it(oauth_service: OAuthService):
    """Test that verify_state is one-time use (consumed)."""
    state = oauth_service.generate_state()
    oauth_service.store_state(state, "google")

    # First call succeeds
    assert oauth_service.verify_state(state) == "google"
    # Second call returns None (consumed)
    assert oauth_service.verify_state(state) is None


def test_verify_unknown_state(oauth_service: OAuthService):
    """Test verifying a non-existent state returns None."""
    result = oauth_service.verify_state("nonexistent-state")
    assert result is None


def test_get_github_auth_url(oauth_service: OAuthService):
    """Test GitHub auth URL generation includes required params."""
    import os
    os.environ["GITHUB_CLIENT_ID"] = "test-client-id"

    from backend.config import settings
    settings.github_client_id = "test-client-id"

    url = oauth_service.get_github_auth_url("test-state")
    assert "github.com/login/oauth/authorize" in url
    assert "test-client-id" in url
    assert "test-state" in url


def test_get_github_auth_url_raises_without_config(oauth_service: OAuthService):
    """Test GitHub auth URL raises when not configured."""
    from backend.config import settings
    original = settings.github_client_id
    settings.github_client_id = None

    with pytest.raises(ValueError, match="GitHub OAuth not configured"):
        oauth_service.get_github_auth_url("state")

    settings.github_client_id = original


def test_get_google_auth_url(oauth_service: OAuthService):
    """Test Google auth URL generation."""
    from backend.config import settings
    settings.google_client_id = "test-google-id"

    url = oauth_service.get_google_auth_url("test-state")
    assert "accounts.google.com" in url
    assert "test-google-id" in url


def test_get_google_auth_url_raises_without_config(oauth_service: OAuthService):
    """Test Google auth URL raises when not configured."""
    from backend.config import settings
    original = settings.google_client_id
    settings.google_client_id = None

    with pytest.raises(ValueError, match="Google OAuth not configured"):
        oauth_service.get_google_auth_url("state")

    settings.google_client_id = original


def test_get_telegram_auth_url(oauth_service: OAuthService):
    """Test Telegram auth URL generation."""
    from backend.config import settings
    settings.telegram_bot_token = "123456:ABC-DEF"

    url = oauth_service.get_telegram_auth_url("test-state")
    assert "oauth.telegram.org/auth" in url


def test_get_telegram_auth_url_raises_without_config(oauth_service: OAuthService):
    """Test Telegram auth URL raises when not configured."""
    from backend.config import settings
    original = settings.telegram_bot_token
    settings.telegram_bot_token = None

    with pytest.raises(ValueError, match="Telegram Bot not configured"):
        oauth_service.get_telegram_auth_url("state")

    settings.telegram_bot_token = original


def test_get_auth_url_dispatches_github(oauth_service: OAuthService):
    """Test get_auth_url dispatches to correct provider method."""
    from backend.config import settings
    settings.github_client_id = "test-id"

    url = oauth_service.get_auth_url("github", "state123")
    assert "github.com" in url


def test_get_auth_url_dispatches_google(oauth_service: OAuthService):
    """Test get_auth_url dispatches to Google."""
    from backend.config import settings
    settings.google_client_id = "test-id"

    url = oauth_service.get_auth_url("google", "state123")
    assert "accounts.google.com" in url


def test_get_auth_url_dispatches_telegram(oauth_service: OAuthService):
    """Test get_auth_url dispatches to Telegram."""
    from backend.config import settings
    settings.telegram_bot_token = "123456:ABC"

    url = oauth_service.get_auth_url("telegram", "state123")
    assert "oauth.telegram.org" in url


def test_get_auth_url_unknown_provider(oauth_service: OAuthService):
    """Test get_auth_url raises for unknown provider."""
    with pytest.raises(ValueError, match="Unknown OAuth provider"):
        oauth_service.get_auth_url("unknown", "state")


@pytest.mark.asyncio
async def test_verify_telegram_auth_success():
    """Test Telegram auth verification returns user info."""
    from backend.config import settings
    settings.telegram_bot_token = "123456:ABC-DEF"

    service = OAuthService()
    result = await service.verify_telegram_auth({
        "id": "12345",
        "first_name": "Test",
        "last_name": "User",
        "photo_url": "https://example.com/pic.jpg",
    })
    assert result is not None
    assert result["provider_user_id"] == "12345"
    assert result["name"] == "Test User"


@pytest.mark.asyncio
async def test_verify_telegram_auth_no_token():
    """Test Telegram auth verification returns None when bot token missing."""
    from backend.config import settings
    original = settings.telegram_bot_token
    settings.telegram_bot_token = None

    service = OAuthService()
    result = await service.verify_telegram_auth({"id": "123"})
    assert result is None

    settings.telegram_bot_token = original


@pytest.mark.asyncio
async def test_get_user_info_github_no_config():
    """Test GitHub user info returns None when not configured."""
    from backend.config import settings
    original_id = settings.github_client_id
    original_secret = settings.github_client_secret
    settings.github_client_id = None
    settings.github_client_secret = None

    service = OAuthService()
    result = await service.get_user_info("github", "any-code")
    assert result is None

    settings.github_client_id = original_id
    settings.github_client_secret = original_secret


@pytest.mark.asyncio
async def test_get_user_info_telegram_returns_none():
    """Test Telegram user info returns None (widget flow, not code exchange)."""
    service = OAuthService()
    result = await service.get_user_info("telegram", "any-code")
    assert result is None
