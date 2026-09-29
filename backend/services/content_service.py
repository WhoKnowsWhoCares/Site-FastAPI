"""Content service for managing page content, projects, and media."""
from typing import Optional
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.content import (
    SectionType,
    ContentType,
    PageContent,
    Project,
    Media,
)
from backend.schemas.content import (
    ContentCreate,
    ContentUpdate,
    ContentRead,
    ContentList,
    ProjectCreate,
    ProjectUpdate,
    ProjectRead,
    MediaRead,
)
from backend.schemas.common import PaginationParams


class ContentService:
    """Service for content management operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # PageContent methods
    async def get_content_by_section(
        self,
        section: SectionType,
        published_only: bool = True,
    ) -> list[PageContent]:
        """Get all content blocks for a section."""
        query = select(PageContent).where(PageContent.section == section)
        if published_only:
            query = query.where(PageContent.is_published == True)
        query = query.order_by(PageContent.order)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_content_by_id(self, content_id: int) -> Optional[PageContent]:
        """Get content by ID."""
        result = await self.db.execute(
            select(PageContent).where(PageContent.id == content_id)
        )
        return result.scalar_one_or_none()

    async def create_content(self, content_data: ContentCreate) -> PageContent:
        """Create new content block."""
        content = PageContent(**content_data.model_dump())
        self.db.add(content)
        await self.db.commit()
        await self.db.refresh(content)
        return content

    async def update_content(
        self,
        content_id: int,
        content_data: ContentUpdate,
    ) -> Optional[PageContent]:
        """Update content block."""
        content = await self.get_content_by_id(content_id)
        if not content:
            return None

        update_data = content_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(content, field, value)

        await self.db.commit()
        await self.db.refresh(content)
        return content

    async def delete_content(self, content_id: int) -> bool:
        """Delete content block."""
        content = await self.get_content_by_id(content_id)
        if not content:
            return False

        await self.db.delete(content)
        await self.db.commit()
        return True

    async def reorder_content(self, section: SectionType, content_orders: list[tuple[int, int]]) -> bool:
        """Reorder content blocks in a section.
        
        Args:
            section: Section to reorder
            content_orders: List of (content_id, new_order) tuples
        """
        for content_id, new_order in content_orders:
            content = await self.get_content_by_id(content_id)
            if content and content.section == section:
                content.order = new_order
        
        await self.db.commit()
        return True

    # Project methods
    async def get_projects_by_section(
        self,
        section: SectionType,
        published_only: bool = True,
    ) -> list[Project]:
        """Get all projects for a section."""
        query = select(Project).where(Project.section == section)
        if published_only:
            query = query.where(Project.is_published == True)
        query = query.order_by(Project.order)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID."""
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_project_by_slug(self, slug: str) -> Optional[Project]:
        """Get project by slug."""
        result = await self.db.execute(
            select(Project).where(Project.slug == slug)
        )
        return result.scalar_one_or_none()

    async def create_project(self, project_data: ProjectCreate) -> Project:
        """Create new project."""
        project = Project(**project_data.model_dump())
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def update_project(
        self,
        project_id: int,
        project_data: ProjectUpdate,
    ) -> Optional[Project]:
        """Update project."""
        project = await self.get_project_by_id(project_id)
        if not project:
            return None

        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)

        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def delete_project(self, project_id: int) -> bool:
        """Delete project."""
        project = await self.get_project_by_id(project_id)
        if not project:
            return False

        await self.db.delete(project)
        await self.db.commit()
        return True

    # Media methods
    async def get_media_by_id(self, media_id: int) -> Optional[Media]:
        """Get media by ID."""
        result = await self.db.execute(
            select(Media).where(Media.id == media_id)
        )
        return result.scalar_one_or_none()

    async def get_media_by_section(
        self,
        section: SectionType,
        pagination: PaginationParams,
    ) -> tuple[list[Media], int]:
        """Get media files for a section with pagination."""
        query = select(Media).where(Media.section == section)
        count_query = select(func.count(Media.id)).where(Media.section == section)

        total = (await self.db.execute(count_query)).scalar() or 0

        query = query.order_by(Media.created_at.desc())
        query = query.offset((pagination.page - 1) * pagination.page_size)
        query = query.limit(pagination.page_size)

        result = await self.db.execute(query)
        items = list(result.scalars().all())

        return items, total

    async def create_media(self, media_data: MediaRead) -> Media:
        """Create new media record."""
        media = Media(**media_data.model_dump())
        self.db.add(media)
        await self.db.commit()
        await self.db.refresh(media)
        return media

    async def delete_media(self, media_id: int) -> bool:
        """Delete media record."""
        media = await self.get_media_by_id(media_id)
        if not media:
            return False

        await self.db.delete(media)
        await self.db.commit()
        return True

    # Public API methods (combined data for frontend)
    async def get_section_data(self, section: SectionType) -> dict:
        """Get all data for a section (content + projects)."""
        content = await self.get_content_by_section(section)
        projects = await self.get_projects_by_section(section)

        return {
            "section": section.value,
            "content": [
                ContentRead.model_validate(c).model_dump() for c in content
            ],
            "projects": [
                ProjectRead.model_validate(p).model_dump() for p in projects
            ],
        }

    async def get_all_sections_data(self) -> dict:
        """Get data for all sections."""
        sections = [SectionType.ABOUTME, SectionType.IHOME, SectionType.TRADE4ME, SectionType.SDART]
        result = {}
        for section in sections:
            result[section.value] = await self.get_section_data(section)
        return result