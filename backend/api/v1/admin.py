"""Admin endpoints: POST/PUT/DELETE /api/v1/admin/content."""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import get_current_admin, get_db
from backend.models.content import SectionType, ContentType
from backend.schemas.content import (
    ContentCreate,
    ContentUpdate,
    ContentRead,
    ProjectCreate,
    ProjectUpdate,
    ProjectRead,
)
from backend.services.content_service import ContentService


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/content", response_model=ContentRead)
async def create_content(
    content_data: ContentCreate,
    admin: dict = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a new content block (admin only)."""
    service = ContentService(db)
    content = await service.create_content(content_data)
    return ContentRead.model_validate(content)


@router.put("/content/{content_id}", response_model=ContentRead)
async def update_content(
    content_id: int,
    content_data: ContentUpdate,
    admin: dict = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a content block (admin only)."""
    service = ContentService(db)
    content = await service.update_content(content_id, content_data)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return ContentRead.model_validate(content)


@router.delete("/content/{content_id}")
async def delete_content(
    content_id: int,
    admin: dict = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete a content block (admin only)."""
    service = ContentService(db)
    deleted = await service.delete_content(content_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"message": "Content deleted successfully"}


@router.post("/project", response_model=ProjectRead)
async def create_project(
    project_data: ProjectCreate,
    admin: dict = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a new project (admin only)."""
    service = ContentService(db)
    project = await service.create_project(project_data)
    return ProjectRead.model_validate(project)


@router.put("/project/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    admin: dict = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a project (admin only)."""
    service = ContentService(db)
    project = await service.update_project(project_id, project_data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectRead.model_validate(project)


@router.delete("/project/{project_id}")
async def delete_project(
    project_id: int,
    admin: dict = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete a project (admin only)."""
    service = ContentService(db)
    deleted = await service.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}


@router.get("/content", response_model=dict)
async def list_all_content(
    section: SectionType = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    admin: dict = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all content blocks (admin only)."""
    service = ContentService(db)
    
    if section:
        items = await service.get_content_by_section(section, published_only=False)
    else:
        from sqlalchemy import select
        from backend.models.content import PageContent
        query = select(PageContent)
        result = await db.execute(query)
        items = list(result.scalars().all())

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


@router.get("/projects", response_model=dict)
async def list_all_projects(
    section: SectionType = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    admin: dict = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all projects (admin only)."""
    service = ContentService(db)
    
    if section:
        items = await service.get_projects_by_section(section, published_only=False)
    else:
        from sqlalchemy import select
        from backend.models.content import Project
        query = select(Project)
        result = await db.execute(query)
        items = list(result.scalars().all())

    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_items = items[start:end]
    
    return {
        "items": [ProjectRead.model_validate(i).model_dump() for i in paginated_items],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if page_size > 0 else 0,
    }


@router.post("/content/reorder")
async def reorder_content(
    section: SectionType,
    content_orders: list[tuple[int, int]],
    admin: dict = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Reorder content blocks in a section (admin only)."""
    service = ContentService(db)
    await service.reorder_content(section, content_orders)
    return {"message": "Content reordered successfully"}
