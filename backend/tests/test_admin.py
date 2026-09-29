"""Integration tests for protected admin endpoints."""
import pytest

from backend.models.content import PageContent
from backend.schemas.content import ContentCreate
from backend.services import content_service


@pytest.mark.asyncio
async def test_admin_list_requires_auth(client):
    resp = await client.get("/api/v1/admin/content")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_admin_create_requires_auth(client):
    resp = await client.post(
        "/api/v1/admin/content",
        json={"section": "aboutme", "slug": "x", "title": "X"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_admin_update_requires_auth(client):
    resp = await client.put(
        "/api/v1/admin/content/aboutme/x", json={"title": "T"}
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_admin_delete_requires_auth(client):
    resp = await client.delete("/api/v1/admin/content/aboutme/x")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_admin_create_and_public_visible(db_session, client, admin_headers):
    resp = await client.post(
        "/api/v1/admin/content",
        json={"section": "aboutme", "slug": "hello", "title": "Hello", "body": "World"},
        headers=admin_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["slug"] == "hello"
    assert data["is_published"] is True

    public = await client.get("/api/v1/content/aboutme")
    assert public.json()["total"] == 1


@pytest.mark.asyncio
async def test_admin_create_duplicate_conflict(db_session, client, admin_headers):
    body = {"section": "ihome", "slug": "dup", "title": "Dup"}
    first = await client.post("/api/v1/admin/content", json=body, headers=admin_headers)
    assert first.status_code == 201
    second = await client.post("/api/v1/admin/content", json=body, headers=admin_headers)
    assert second.status_code == 409


@pytest.mark.asyncio
async def test_admin_list_returns_all_sections(db_session, client, admin_headers):
    for section in ("aboutme", "ihome", "trade4me", "sdart"):
        await content_service.create_content(
            db_session,
            ContentCreate(section=section, slug="item", title=f"{section} item"),
        )
    resp = await client.get("/api/v1/admin/content", headers=admin_headers)
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 4
    assert {i["section"] for i in items} == {"aboutme", "ihome", "trade4me", "sdart"}


@pytest.mark.asyncio
async def test_admin_list_includes_unpublished(db_session, client, admin_headers):
    await content_service.create_content(
        db_session,
        ContentCreate(section="sdart", slug="draft", title="Draft", is_published=False),
    )
    resp = await client.get("/api/v1/admin/content", headers=admin_headers)
    slugs = [i["slug"] for i in resp.json()]
    assert "draft" in slugs


@pytest.mark.asyncio
async def test_admin_update_content(db_session, client, admin_headers):
    await content_service.create_content(
        db_session,
        ContentCreate(section="trade4me", slug="stats", title="Old"),
    )
    resp = await client.put(
        "/api/v1/admin/content/trade4me/stats",
        json={"title": "New", "is_published": False},
        headers=admin_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "New"
    assert data["is_published"] is False


@pytest.mark.asyncio
async def test_admin_update_missing_404(client, admin_headers):
    resp = await client.put(
        "/api/v1/admin/content/aboutme/ghost", json={"title": "T"}, headers=admin_headers
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_admin_delete_content(db_session, client, admin_headers):
    await content_service.create_content(
        db_session,
        ContentCreate(section="sdart", slug="temp", title="Temp"),
    )
    resp = await client.delete(
        "/api/v1/admin/content/sdart/temp", headers=admin_headers
    )
    assert resp.status_code == 204
    public = await client.get("/api/v1/content/sdart")
    assert public.json()["total"] == 0


@pytest.mark.asyncio
async def test_admin_delete_missing_404(client, admin_headers):
    resp = await client.delete(
        "/api/v1/admin/content/sdart/ghost", headers=admin_headers
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_admin_invalid_token_401(client):
    resp = await client.get(
        "/api/v1/admin/content", headers={"Authorization": "Bearer wrong-token"}
    )
    assert resp.status_code == 401
