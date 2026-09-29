"""Integration tests for public content endpoints."""
import pytest

from backend.models.content import PageContent
from backend.schemas.content import ContentCreate
from backend.services import content_service

SECTIONS = ("aboutme", "ihome", "trade4me", "sdart")


async def seed_content(db_session, section: str, slug: str = "intro", **kwargs) -> PageContent:
    payload = ContentCreate(
        section=section, slug=slug, title=kwargs.pop("title", f"{section} title"), **kwargs
    )
    return await content_service.create_content(db_session, payload)


# --- Service-level tests ---------------------------------------------------

@pytest.mark.asyncio
async def test_create_and_get_content(db_session):
    created = await seed_content(db_session, "aboutme")
    fetched = await content_service.get_content(db_session, "aboutme", "intro")
    assert fetched.id == created.id
    assert fetched.title == "aboutme title"


@pytest.mark.asyncio
async def test_duplicate_section_slug_raises(db_session):
    await seed_content(db_session, "aboutme")
    with pytest.raises(content_service.DuplicateContentError):
        await seed_content(db_session, "aboutme")


@pytest.mark.asyncio
async def test_missing_content_raises(db_session):
    with pytest.raises(content_service.ContentNotFoundError):
        await content_service.get_content(db_session, "aboutme", "nope")


@pytest.mark.asyncio
async def test_unpublished_hidden_from_public_listing(db_session):
    await seed_content(db_session, "sdart", slug="visible")
    await seed_content(db_session, "sdart", slug="hidden", is_published=False)
    items = await content_service.list_content(db_session, "sdart")
    assert [i.slug for i in items] == ["visible"]


@pytest.mark.asyncio
async def test_update_content_partial(db_session):
    await seed_content(db_session, "ihome")
    from backend.schemas.content import ContentUpdate

    updated = await content_service.update_content(
        db_session, "ihome", "intro", ContentUpdate(title="New title", body="Body text")
    )
    assert updated.title == "New title"
    assert updated.body == "Body text"


@pytest.mark.asyncio
async def test_delete_content(db_session):
    await seed_content(db_session, "trade4me")
    await content_service.delete_content(db_session, "trade4me", "intro")
    with pytest.raises(content_service.ContentNotFoundError):
        await content_service.get_content(db_session, "trade4me", "intro")


# --- API integration tests ---------------------------------------------------

@pytest.mark.asyncio
async def test_get_section_content_empty(client):
    for section in SECTIONS:
        resp = await client.get(f"/api/v1/content/{section}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["section"] == section
        assert data["items"] == []
        assert data["total"] == 0


@pytest.mark.asyncio
async def test_get_section_content_returns_seeded(db_session, client):
    await seed_content(db_session, "aboutme", slug="bio", title="Bio")
    resp = await client.get("/api/v1/content/aboutme")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["slug"] == "bio"
    assert data["items"][0]["title"] == "Bio"


@pytest.mark.asyncio
async def test_get_content_by_slug(db_session, client):
    await seed_content(db_session, "sdart", slug="gallery", title="Gallery")
    resp = await client.get("/api/v1/content/sdart/gallery")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Gallery"


@pytest.mark.asyncio
async def test_get_content_unknown_slug_404(client):
    resp = await client.get("/api/v1/content/aboutme/missing")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_unknown_section_404(client):
    resp = await client.get("/api/v1/content/unknown")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_ordering_by_order_field(db_session, client):
    await seed_content(db_session, "ihome", slug="b", order=2)
    await seed_content(db_session, "ihome", slug="a", order=1)
    resp = await client.get("/api/v1/content/ihome")
    slugs = [i["slug"] for i in resp.json()["items"]]
    assert slugs == ["a", "b"]
