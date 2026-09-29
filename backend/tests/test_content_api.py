"""Integration tests for public content API endpoints."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.content import SectionType, ContentType, PageContent, Project


@pytest.mark.asyncio
async def test_list_content_empty(client: AsyncClient):
    """Test listing content returns empty when no data exists."""
    response = await client.get("/api/content/")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1


@pytest.mark.asyncio
async def test_list_content_with_filter(client: AsyncClient, test_db: AsyncSession):
    """Test filtering content by section."""
    content = PageContent(
        section=SectionType.ABOUTME,
        content_type=ContentType.TEXT,
        title="About",
        body="About me text",
        order=1,
        is_published=True,
    )
    test_db.add(content)
    await test_db.commit()

    response = await client.get("/api/content/", params={"section": "aboutme"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "About"


@pytest.mark.asyncio
async def test_list_content_pagination(client: AsyncClient, test_db: AsyncSession):
    """Test pagination of content list."""
    for i in range(5):
        c = PageContent(
            section=SectionType.ABOUTME,
            content_type=ContentType.TEXT,
            title=f"Item {i}",
            order=i,
            is_published=True,
        )
        test_db.add(c)
    await test_db.commit()

    response = await client.get("/api/content/", params={"page": 1, "page_size": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total_pages"] == 3


@pytest.mark.asyncio
async def test_get_section_content(client: AsyncClient, test_db: AsyncSession):
    """Test getting all content for a specific section."""
    content = PageContent(
        section=SectionType.IHOME,
        content_type=ContentType.HERO,
        title="Home Hero",
        body="Welcome home",
        order=1,
        is_published=True,
    )
    test_db.add(content)
    await test_db.commit()

    response = await client.get("/api/content/ihome")
    assert response.status_code == 200
    data = response.json()
    assert data["section"] == "ihome"
    assert len(data["content"]) == 1
    assert data["projects"] == []


@pytest.mark.asyncio
async def test_get_content_item(client: AsyncClient, test_db: AsyncSession):
    """Test getting a specific content item by section and slug."""
    project = Project(
        section=SectionType.TRADE4ME,
        title="Trade Project",
        slug="trade-project",
        description="A trading project",
        is_published=True,
    )
    test_db.add(project)
    await test_db.commit()

    response = await client.get("/api/content/trade4me/trade-project")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Trade Project"


@pytest.mark.asyncio
async def test_get_content_item_not_found(client: AsyncClient):
    """Test 404 for non-existent content item."""
    response = await client.get("/api/content/aboutme/nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_sections(client: AsyncClient, test_db: AsyncSession):
    """Test getting data for all sections."""
    content = PageContent(
        section=SectionType.ABOUTME,
        content_type=ContentType.TEXT,
        title="About",
        is_published=True,
    )
    test_db.add(content)
    await test_db.commit()

    response = await client.get("/api/content/all-sections")
    assert response.status_code == 200
    data = response.json()
    assert "aboutme" in data


@pytest.mark.asyncio
async def test_list_content_unpublished_excluded(client: AsyncClient, test_db: AsyncSession):
    """Test that unpublished content is excluded from public list."""
    published = PageContent(
        section=SectionType.SDART,
        content_type=ContentType.TEXT,
        title="Published",
        is_published=True,
    )
    unpublished = PageContent(
        section=SectionType.SDART,
        content_type=ContentType.TEXT,
        title="Draft",
        is_published=False,
    )
    test_db.add_all([published, unpublished])
    await test_db.commit()

    response = await client.get("/api/content/", params={"section": "sdart"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Published"
