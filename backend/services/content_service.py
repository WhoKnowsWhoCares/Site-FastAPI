"""Content CRUD service for PageContent, Project, Media."""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.content import Media, PageContent, Project
from backend.schemas.content import ContentCreate, ContentUpdate

SECTION_REQUIRED = False  # sections are open strings; validated at API layer


class ContentNotFoundError(Exception):
    """Raised when a content block does not exist."""


class DuplicateContentError(Exception):
    """Raised when a (section, slug) pair already exists."""


# --- PageContent -----------------------------------------------------------

async def list_content(
    db: AsyncSession, section: str, include_unpublished: bool = False
) -> list[PageContent]:
    """List content blocks for a section ordered by 'order', then id."""
    stmt = select(PageContent).where(PageContent.section == section)
    if not include_unpublished:
        stmt = stmt.where(PageContent.is_published.is_(True))
    stmt = stmt.order_by(PageContent.order, PageContent.id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def count_content(
    db: AsyncSession, section: str, include_unpublished: bool = False
) -> int:
    """Count content blocks for a section."""
    stmt = (
        select(func.count())
        .select_from(PageContent)
        .where(PageContent.section == section)
    )
    if not include_unpublished:
        stmt = stmt.where(PageContent.is_published.is_(True))
    result = await db.execute(stmt)
    return int(result.scalar_one())


async def get_content(
    db: AsyncSession, section: str, slug: str, include_unpublished: bool = False
) -> PageContent:
    """Fetch a single content block by section and slug."""
    stmt = select(PageContent).where(
        PageContent.section == section, PageContent.slug == slug
    )
    if not include_unpublished:
        stmt = stmt.where(PageContent.is_published.is_(True))
    result = await db.execute(stmt)
    content = result.scalar_one_or_none()
    if content is None:
        raise ContentNotFoundError(f"{section}/{slug} not found")
    return content


async def create_content(db: AsyncSession, payload: ContentCreate) -> PageContent:
    """Create a content block; (section, slug) must be unique."""
    stmt = select(PageContent).where(
        PageContent.section == payload.section, PageContent.slug == payload.slug
    )
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing is not None:
        raise DuplicateContentError(f"{payload.section}/{payload.slug} already exists")

    content = PageContent(**payload.model_dump())
    db.add(content)
    await db.commit()
    await db.refresh(content)
    return content


async def update_content(
    db: AsyncSession, section: str, slug: str, payload: ContentUpdate
) -> PageContent:
    """Partially update a content block (including unpublished drafts)."""
    content = await get_content(db, section, slug, include_unpublished=True)
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(content, field, value)
    db.add(content)
    await db.commit()
    await db.refresh(content)
    return content


async def delete_content(db: AsyncSession, section: str, slug: str) -> None:
    """Delete a content block; raises ContentNotFoundError when missing."""
    content = await get_content(db, section, slug, include_unpublished=True)
    await db.delete(content)
    await db.commit()


# --- Project ---------------------------------------------------------------

async def list_projects(
    db: AsyncSession, section: str | None = None, include_unpublished: bool = False
) -> list[Project]:
    """List projects, optionally filtered by section."""
    stmt = select(Project)
    if section is not None:
        stmt = stmt.where(Project.section == section)
    if not include_unpublished:
        stmt = stmt.where(Project.is_published.is_(True))
    stmt = stmt.order_by(Project.order, Project.id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_project(
    db: AsyncSession,
    *,
    name: str,
    section: str,
    description: str = "",
    url: str | None = None,
    order: int = 0,
    is_published: bool = True,
) -> Project:
    """Create a project entry."""
    project = Project(
        name=name,
        section=section,
        description=description,
        url=url,
        order=order,
        is_published=is_published,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project_id: int) -> None:
    """Delete a project by id."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if project is None:
        raise ContentNotFoundError(f"project {project_id} not found")
    await db.delete(project)
    await db.commit()


# --- Media -----------------------------------------------------------------

async def list_media(db: AsyncSession, project_id: int | None = None) -> list[Media]:
    """List media items, optionally filtered by project."""
    stmt = select(Media).order_by(Media.order, Media.id)
    if project_id is not None:
        stmt = stmt.where(Media.project_id == project_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_media(
    db: AsyncSession,
    *,
    url: str,
    kind: str = "image",
    alt: str = "",
    project_id: int | None = None,
    order: int = 0,
) -> Media:
    """Create a media item, optionally attached to a project."""
    media = Media(url=url, kind=kind, alt=alt, project_id=project_id, order=order)
    db.add(media)
    await db.commit()
    await db.refresh(media)
    return media


async def delete_media(db: AsyncSession, media_id: int) -> None:
    """Delete a media item by id."""
    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalar_one_or_none()
    if media is None:
        raise ContentNotFoundError(f"media {media_id} not found")
    await db.delete(media)
    await db.commit()
