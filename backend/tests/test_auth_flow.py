"""Integration tests: full OAuth callback flow with mocked provider HTTP calls,
token issuance, and use of the issued token on /auth/me."""
import backend.services.oauth_service as oauth_svc


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload
        self.status_code = 200

    def json(self):
        return self._payload


class _FakeAsyncClient:
    """Replaces httpx.AsyncClient inside oauth_service only (test client unaffected)."""

    def __init__(self, post_payloads=None, get_payloads=None):
        self._post_payloads = post_payloads or {}
        self._get_payloads = get_payloads or {}
        self.post_calls: list[tuple] = []
        self.get_calls: list[tuple] = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def post(self, url, **kwargs):
        self.post_calls.append((url, kwargs))
        for match, payload in self._post_payloads.items():
            if match in url:
                return _FakeResponse(payload)
        return _FakeResponse({})

    async def get(self, url, **kwargs):
        self.get_calls.append((url, kwargs))
        for match, payload in self._get_payloads.items():
            if match in url:
                return _FakeResponse(payload)
        return _FakeResponse({})


GITHUB_TOKEN_RESPONSE = {"access_token": "gho_test_token"}
GITHUB_USER = {"id": 12345, "login": "alex", "name": "Alexander", "email": None}
GITHUB_EMAILS = [{"email": "alex@example.com", "primary": True, "verified": True}]


def _patch_github(monkeypatch):
    provider = oauth_svc.get_provider("github")
    monkeypatch.setattr(provider, "client_id", "test-gh-id")
    monkeypatch.setattr(provider, "client_secret", "test-gh-secret")

    def factory(**kwargs):
        return _FakeAsyncClient(
            post_payloads={"access_token": GITHUB_TOKEN_RESPONSE},
            get_payloads={
                "api.github.com/user/emails": GITHUB_EMAILS,
                "api.github.com/user": GITHUB_USER,
            },
        )

    monkeypatch.setattr(oauth_svc.httpx, "AsyncClient", factory)


def _patch_google(monkeypatch):
    provider = oauth_svc.get_provider("google")
    monkeypatch.setattr(provider, "client_id", "test-goog-id")
    monkeypatch.setattr(provider, "client_secret", "test-goog-secret")

    def factory(**kwargs):
        return _FakeAsyncClient(
            post_payloads={"oauth2.googleapis.com": {"access_token": "goog_token"}},
            get_payloads={
                "openidconnect.googleapis.com": {
                    "sub": "goog-99",
                    "email": "alex@gmail.com",
                    "name": "Alexander G",
                }
            },
        )

    monkeypatch.setattr(oauth_svc.httpx, "AsyncClient", factory)


class TestCallbackFullFlow:
    async def test_github_callback_creates_user_and_returns_token(self, client, monkeypatch):
        _patch_github(monkeypatch)

        resp = await client.post(
            "/api/v1/auth/callback/github",
            json={"code": "good-code", "state": "st"},
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data["token_type"] == "bearer"
        assert data["access_token"]

        # Issued token works on /me and returns the created user
        me = await client.get(
            "/api/v1/auth/me", headers={"Authorization": f"Bearer {data['access_token']}"}
        )
        assert me.status_code == 200
        assert me.json()["email"] == "alex@example.com"
        assert me.json()["name"] == "Alexander"

    async def test_callback_is_idempotent_for_same_provider_identity(self, client, monkeypatch):
        _patch_github(monkeypatch)

        body = {"code": "code-1", "state": "st"}
        r1 = await client.post("/api/v1/auth/callback/github", json=body)
        r2 = await client.post("/api/v1/auth/callback/github", json=body)
        assert r1.status_code == r2.status_code == 200

        me1 = await client.get(
            "/api/v1/auth/me", headers={"Authorization": f"Bearer {r1.json()['access_token']}"}
        )
        me2 = await client.get(
            "/api/v1/auth/me", headers={"Authorization": f"Bearer {r2.json()['access_token']}"}
        )
        assert me1.json()["id"] == me2.json()["id"]

    async def test_google_callback_creates_user(self, client, monkeypatch):
        _patch_google(monkeypatch)

        resp = await client.post(
            "/api/v1/auth/callback/google", json={"code": "c", "state": "s"}
        )
        assert resp.status_code == 200, resp.text
        me = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {resp.json()['access_token']}"},
        )
        assert me.json()["email"] == "alex@gmail.com"
