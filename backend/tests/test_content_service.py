"""Integration tests for content service methods."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.content import SectionType, ContentType, PageContent, Project
from backend.schemas.content import ContentCreate, ContentUpdate, ProjectCreate, ProjectUpdate
from backend.services.content_service import ContentService


@pytest.mark.asyncio
async def test_get_content_by_section(test_db: AsyncSession):
    """Test getting content blocks for a specific section."""
    c1 = PageContent(
        section=SectionType.ABOUTME,
        content_type=ContentType.TEXT,
        title="First",
        order=1,
        is_published=True,
    )
    c2 = PageContent(
        section=SectionType.ABOUTME,
        content_type=ContentType.IMAGE,
        title="Second",
        order=2,
        is_published=True,
    )
    test_db.add_all([c1, c2])
    await test_db.commit()

    service = ContentService(test_db)
    result = await service.get_content_by_section(SectionType.ABOUTME)
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_content_by_id(test_db: AsyncSession):
    """Test getting a single content block by ID."""
    content = PageContent(
        section=SectionType.IHOME,
        content_type=ContentType.HERO,
        title="Hero Block",
    )
    test_db.add(content)
    await test_db.commit()
    await test_db.refresh(content)

    service = ContentService(test_db)
    result = await service.get_content_by_id(content.id)
    assert result is not None
    assert result.title == "Hero Block"


@pytest.mark.asyncio
async def test_get_content_by_id_not_found(test_db: AsyncSession):
    """Test getting non-existent content returns None."""
    service = ContentService(test_db)
    result = await service.get_content_by_id(99999)
    assert result is None


@pytest.mark.asyncio
async def test_create_content(test_db: AsyncSession):
    """Test creating a new content block."""
    from backend.schemas.content import ContentCreate

    data = ContentCreate(
        section="sdart",
        content_type="card",
        title="New Card",
        body="Card body",
    )
    service = ContentService(test_db)
    result = await service.create_content(data)
    assert result.id is not None
    assert result.title == "New Card"


@pytest.mark.asyncio
async def test_update_content(test_db: AsyncSession):
    """Test updating an existing content block."""
    from backend.schemas.content import ContentUpdate

    content = PageContent(
        section=SectionType.ABOUTME,
        content_type=ContentType.TEXT,
        title="Original",
    )
    test_db.add(content)
    await test_db.commit()
    await test_db.refresh(content)

    service = ContentService(test_db)
    result = await service.update_content(content.id, ContentUpdate(title="Updated"))
    assert result is not None
    assert result.title == "Updated"


@pytest.mark.asyncio
async def test_update_content_not_found(test_db: AsyncSession):
    """Test updating non-existent content returns None."""
    from backend.schemas.content import ContentUpdate

    service = ContentService(test_db)
    result = await service.update_content(99999, ContentUpdate(title="Nope"))
    assert result is None


@pytest.mark.asyncio
async def test_delete_content(test_db: AsyncSession):
    """Test deleting a content block."""
    content = PageContent(
        section=SectionType.IHOME,
        content_type=ContentType.TEXT,
        title="To Delete",
    )
    test_db.add(content)
    await test_db.commit()
    await test_db.refresh(content)

    service = ContentService(test_db)
    result = await service.delete_content(content.id)
    assert result is True


@pytest.mark.asyncio
async def test_delete_content_not_found(test_db: AsyncSession):
    """Test deleting non-existent content returns False."""
    service = ContentService(test_db)
    result = await service.delete_content(99999)
    assert result is False


@pytest.mark.asyncio
async def test_get_projects_by_section(test_db: AsyncSession):
    """Test getting projects for a section."""
    p1 = Project(section=SectionType.TRADE4ME, title="Proj 1", slug="proj-1")
    p2 = Project(section=SectionType.TRADE4ME, title="Proj 2", slug="proj-2")
    test_db.add_all([p1, p2])
    await test_db.commit()

    service = ContentService(test_db)
    result = await service.get_projects_by_section(SectionType.TRADE4ME)
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_project_by_slug(test_db: AsyncSession):
    """Test getting a project by its slug."""
    project = Project(
        section=SectionType.SDART,
        title="Slug Test",
        slug="my-slug-project",
    )
    test_db.add(project)
    await test_db.commit()

    service = ContentService(test_db)
    result = await service.get_project_by_slug("my-slug-project")
    assert result is not None
    assert result.title == "Slug Test"


@pytest.mark.asyncio
async def test_create_project(test_db: AsyncSession):
    """Test creating a new project."""
    from backend.schemas.content import ProjectCreate

    data = ProjectCreate(
        section=SectionType.IHOME,
        title="New Home Project",
        slug="new-home-project",
        description="A new project",
    )
    service = ContentService(test_db)
    result = await service.create_project(data)
    assert result.id is not None
    assert result.slug == "new-home-project"


@pytest.mark.asyncio
async def test_update_project(test_db: AsyncSession):
    """Test updating a project."""
    from backend.schemas.content import ProjectUpdate

    project = Project(
        section=SectionType.ABOUTME,
        title="Original",
        slug="original-project",
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    service = ContentService(test_db)
    result = await service.update_project(
        project.id, ProjectUpdate(title="Updated Project")
    )
    assert result is not None
    assert result.title == "Updated Project"


@pytest.mark.asyncio
async def test_delete_project(test_db: AsyncSession):
    """Test deleting a project."""
    project = Project(
        section=SectionType.SDART,
        title="Delete Me",
        slug="delete-me",
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    service = ContentService(test_db)
    result = await service.delete_project(project.id)
    assert result is True


@pytest.mark.asyncio
async def test_delete_project_not_found(test_db: AsyncSession):
    """Test deleting non-existent project returns False."""
    service = ContentService(test_db)
    result = await service.delete_project(99999)
    assert result is False


@pytest.mark.asyncio
async def test_get_section_data(test_db: AsyncSession):
    """Test getting combined section data (content + projects)."""
    content = PageContent(
        section=SectionType.ABOUTME,
        content_type=ContentType.TEXT,
        title="About Content",
        is_published=True,
    )
    project = Project(
        section=SectionType.ABOUTME,
        title="About Project",
        slug="about-proj",
    )
    test_db.add_all([content, project])
    await test_db.commit()

    service = ContentService(test_db)
    result = await service.get_section_data(SectionType.ABOUTME)
    assert result["section"] == "aboutme"
    assert len(result["content"]) >= 1
    assert len(result["projects"]) >= 1


@pytest.mark.asyncio
async def test_get_all_sections_data(test_db: AsyncSession):
    """Test getting data for all sections."""
    service = ContentService(test_db)
    result = await service.get_all_sections_data()
    assert "aboutme" in result
    assert "ihome" in result
    assert "trade4me" in result
    assert "sdart" in result


@pytest.mark.asyncio
async def test_reorder_content(test_db: AsyncSession):
    """Test reordering content blocks within a section."""
    c1 = PageContent(
        section=SectionType.IHOME,
        content_type=ContentType.TEXT,
        title="Item 1",
        order=0,
    )
    c2 = PageContent(
        section=SectionType.IHOME,
        content_type=ContentType.TEXT,
        title="Item 2",
        order=1,
    )
    test_db.add_all([c1, c2])
    await test_db.commit()
    await test_db.refresh(c1)
    await test_db.refresh(c2)

    service = ContentService(test_db)
    result = await service.reorder_content(
        SectionType.IHOME, [(c1.id, 10), (c2.id, 5)]
    )
    assert result is True

    # Verify order changed
    updated_c1 = await service.get_content_by_id(c1.id)
    assert updated_c1.order == 10
    updated_c2 = await service.get_content_by_id(c2.id)
    assert updated_c2.order == 5


@pytest.mark.asyncio
async def test_get_projects_by_section_published_filter(test_db: AsyncSession):
    """Test that published_only=False returns all projects."""
    p_pub = Project(
        section=SectionType.SDART,
        title="Published",
        slug="pub-sd",
        is_published=True,
    )
    p_draft = Project(
        section=SectionType.SDART,
        title="Draft",
        slug="draft-sd",
        is_published=False,
    )
    test_db.add_all([p_pub, p_draft])
    await test_db.commit()

    service = ContentService(test_db)
    published_only = await service.get_projects_by_section(
        SectionType.SDART, published_only=True
    )
    all_projects = await service.get_projects_by_section(
        SectionType.SDART, published_only=False
    )
    assert len(published_only) == 1
    assert len(all_projects) == 2
