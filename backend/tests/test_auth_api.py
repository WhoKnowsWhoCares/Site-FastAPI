"""Integration tests for /api/v1/auth endpoints and get_current_user dependency."""
import pytest
from fastapi import HTTPException

from backend.api.deps import get_current_admin, get_current_user


class TestOAuthUrlEndpoint:
    async def test_github_oauth_url(self, client):
        resp = await client.post("/api/v1/auth/oauth/github")
        assert resp.status_code == 200
        data = resp.json()
        assert data["provider"] == "github"
        assert data["url"].startswith("https://github.com/login/oauth/authorize")
        assert data["state"]

    async def test_google_oauth_url(self, client):
        resp = await client.post("/api/v1/auth/oauth/google")
        assert resp.status_code == 200
        assert resp.json()["url"].startswith("https://accounts.google.com/o/oauth2/v2/auth")

    async def test_telegram_oauth_url(self, client):
        resp = await client.post("/api/v1/auth/oauth/telegram")
        assert resp.status_code == 200
        assert "bot_id=" in resp.json()["url"]

    async def test_unknown_provider_404(self, client):
        resp = await client.post("/api/v1/auth/oauth/facebook")
        assert resp.status_code == 404


class TestCallbackEndpoint:
    async def test_github_callback_without_credentials_501(self, client, monkeypatch):
        import backend.services.oauth_service as svc

        provider = svc.get_provider("github")
        saved = provider.client_secret
        provider.client_secret = None
        try:
            resp = await client.post(
                "/api/v1/auth/callback/github",
                json={"code": "abc", "state": "xyz"},
            )
            assert resp.status_code == 501
        finally:
            provider.client_secret = saved

    async def test_unknown_provider_callback_404(self, client):
        resp = await client.post(
            "/api/v1/auth/callback/facebook",
            json={"code": "abc", "state": "xyz"},
        )
        assert resp.status_code == 404


class TestMeAndLogout:
    def _auth_headers(self, token):
        return {"Authorization": f"Bearer {token}"}

    async def test_me_returns_user_for_valid_token(self, client, user, token_factory):
        resp = await client.get("/api/v1/auth/me", headers=self._auth_headers(token_factory(user)))
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == user.email
        assert "id" in data and "is_active" in data

    async def test_me_rejects_missing_token(self, client):
        resp = await client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    async def test_me_rejects_garbage_token(self, client):
        resp = await client.get("/api/v1/auth/me", headers=self._auth_headers("garbage"))
        assert resp.status_code == 401

    async def test_me_rejects_unknown_user(self, client, token_factory):
        from backend.services.auth_service import create_access_token

        token = create_access_token({"sub": "999999"})
        resp = await client.get("/api/v1/auth/me", headers=self._auth_headers(token))
        assert resp.status_code == 401

    async def test_logout_returns_ok(self, client):
        resp = await client.post("/api/v1/auth/logout")
        assert resp.status_code == 200


class TestAdminDependency:
    async def test_admin_dependency_allows_admin(self, session, admin_user, token_factory):
        from backend.services.auth_service import create_access_token

        token = create_access_token({"sub": str(admin_user.id)})
        user = await get_current_user(token=token, db=session)
        admin = await get_current_admin(user=user)
        assert admin.id == admin_user.id

    async def test_admin_dependency_rejects_regular_user(self, session, user):
        with pytest.raises(HTTPException) as exc:
            await get_current_admin(user=user)
        assert exc.value.status_code == 403
