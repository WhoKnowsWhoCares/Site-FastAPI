"""Unit tests for Project and Media service CRUD."""
import pytest

from backend.services import content_service
from backend.services.content_service import ContentNotFoundError


@pytest.mark.asyncio
async def test_project_crud_roundtrip(db_session):
    created = await content_service.create_project(
        db_session, name="iHome", section="ihome", description="Smart home dashboard"
    )
    assert created.id is not None

    projects = await content_service.list_projects(db_session, section="ihome")
    assert [p.name for p in projects] == ["iHome"]

    await content_service.delete_project(db_session, created.id)
    assert await content_service.list_projects(db_session) == []


@pytest.mark.asyncio
async def test_delete_missing_project_raises(db_session):
    with pytest.raises(ContentNotFoundError):
        await content_service.delete_project(db_session, 999)


@pytest.mark.asyncio
async def test_unpublished_project_hidden(db_session):
    await content_service.create_project(
        db_session, name="Visible", section="sdart", is_published=True
    )
    await content_service.create_project(
        db_session, name="Hidden", section="sdart", is_published=False
    )
    projects = await content_service.list_projects(db_session, section="sdart")
    assert [p.name for p in projects] == ["Visible"]


@pytest.mark.asyncio
async def test_media_crud_and_project_link(db_session):
    project = await content_service.create_project(db_session, name="Gallery", section="sdart")
    media = await content_service.create_media(
        db_session, url="https://example.com/a.png", project_id=project.id, alt="A"
    )
    orphan = await content_service.create_media(db_session, url="https://example.com/b.png")

    assert media.project_id == project.id
    assert len(await content_service.list_media(db_session, project_id=project.id)) == 1
    assert len(await content_service.list_media(db_session)) == 2
    assert orphan.project_id is None

    await content_service.delete_media(db_session, media.id)
    with pytest.raises(ContentNotFoundError):
        await content_service.delete_media(db_session, media.id)
