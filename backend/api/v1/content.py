"""Public content endpoints: GET /api/v1/content/{section}."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_db
from backend.models.content import SectionType, PageContent
from backend.schemas.content import ContentRead, ProjectRead, ContentType
from backend.services.content_service import ContentService


router = APIRouter(prefix="/content", tags=["content"])


@router.get("/")
async def list_content(
    section: SectionType = Query(default=None, description="Filter by section"),
    content_type: ContentType = Query(default=None, description="Filter by content type"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all content blocks with optional filters."""
    service = ContentService(db)
    
    if section:
        items = await service.get_content_by_section(section)
    else:
        query = select(PageContent).where(PageContent.is_published == True)
        if content_type:
            query = query.where(PageContent.content_type == content_type)
        query = query.order_by(PageContent.order)
        result = await db.execute(query)
        items = list(result.scalars().all())

    # Pagination
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_items = items[start:end]
    
    return {
        "items": [ContentRead.model_validate(i).model_dump() for i in paginated_items],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if page_size > 0 else 0,
    }


@router.get("/{section}")
async def get_section_content(
    section: SectionType,
    db: AsyncSession = Depends(get_db),
):
    """Get all content for a specific section."""
    service = ContentService(db)
    content = await service.get_content_by_section(section)
    projects = await service.get_projects_by_section(section)
    
    return {
        "section": section.value,
        "content": [ContentRead.model_validate(c).model_dump() for c in content],
        "projects": [ProjectRead.model_validate(p).model_dump() for p in projects],
    }


@router.get("/{section}/{slug}")
async def get_content_item(
    section: SectionType,
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific content item by section and slug."""
    service = ContentService(db)
    
    # Try to find as project first
    project = await service.get_project_by_slug(slug)
    if project and project.section == section:
        return ProjectRead.model_validate(project).model_dump()
    
    # Try to find as content block
    query = select(PageContent).where(
        PageContent.section == section,
        PageContent.title == slug,  # Using title as simple slug
        PageContent.is_published == True,
    )
    result = await db.execute(query)
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(
            status_code=404,
            detail=f"Content not found in section {section.value}",
        )
    
    return ContentRead.model_validate(content).model_dump()


@router.get("/all-sections")
async def get_all_sections(
    db: AsyncSession = Depends(get_db),
):
    """Get data for all sections."""
    service = ContentService(db)
    return await service.get_all_sections_data()
