"""Integration tests for auth API endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_oauth_url(client: AsyncClient, mock_oauth_settings):
    """Test getting OAuth authorization URL returns 200."""
    response = await client.get("/api/auth/oauth/github/url")
    assert response.status_code == 200
    data = response.json()
    assert "authorization_url" in data
    assert "state" in data


@pytest.mark.asyncio
async def test_get_oauth_url_google(client: AsyncClient, mock_oauth_settings):
    """Test getting Google OAuth URL."""
    response = await client.get("/api/auth/oauth/google/url")
    assert response.status_code == 200
    data = response.json()
    assert "github" not in data["authorization_url"]


@pytest.mark.asyncio
async def test_get_oauth_url_telegram(client: AsyncClient, mock_oauth_settings):
    """Test getting Telegram OAuth URL."""
    response = await client.get("/api/auth/oauth/telegram/url")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_oauth_url_invalid_provider(client: AsyncClient):
    """Test invalid OAuth provider returns 400."""
    response = await client.get("/api/auth/oauth/invalid/url")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_me_requires_auth(client: AsyncClient):
    """Test that /me endpoint requires authentication."""
    response = await client.get("/api/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_returns_user(client: AsyncClient, admin_token: str):
    """Test that /me returns current user info with valid token."""
    response = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["is_admin"] is True


@pytest.mark.asyncio
async def test_logout(client: AsyncClient):
    """Test logout endpoint returns success message."""
    response = await client.post("/api/auth/logout")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


@pytest.mark.asyncio
async def test_login_not_implemented(client: AsyncClient):
    """Test that email/password login returns 501."""
    response = await client.post(
        "/api/auth/login",
        json={"code": "test@example.com", "state": ""},
    )
    assert response.status_code == 501


@pytest.mark.asyncio
async def test_get_sections(client: AsyncClient):
    """Test getting available content sections."""
    response = await client.get("/api/auth/sections")
    assert response.status_code == 200
    data = response.json()
    assert "aboutme" in data
    assert "ihome" in data
    assert "trade4me" in data
    assert "sdart" in data
