"""Protected admin endpoints: /api/v1/admin/*."""
from fastapi import APIRouter, HTTPException, status

from backend.api.deps import AdminUser, Db
from backend.schemas.content import ContentCreate, ContentList, ContentRead, ContentUpdate
from backend.services import content_service
from backend.services.content_service import (
    ContentNotFoundError,
    DuplicateContentError,
)

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[])


@router.get("/content", response_model=list[ContentRead])
async def list_all_content(
    admin: AdminUser,
    db: Db,
    include_unpublished: bool = True,
) -> list[ContentRead]:
    """List all content blocks across sections (admin view)."""
    items: list[ContentRead] = []
    for section in ("aboutme", "ihome", "trade4me", "sdart"):
        rows = await content_service.list_content(
            db, section, include_unpublished=include_unpublished
        )
        items.extend(ContentRead.model_validate(r) for r in rows)
    return items


@router.post("/content", response_model=ContentRead, status_code=201)
async def create_content(payload: ContentCreate, admin: AdminUser, db: Db) -> ContentRead:
    """Create a content block."""
    try:
        item = await content_service.create_content(db, payload)
    except DuplicateContentError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return ContentRead.model_validate(item)


@router.put("/content/{section}/{slug}", response_model=ContentRead)
async def update_content(
    section: str, slug: str, payload: ContentUpdate, admin: AdminUser, db: Db
) -> ContentRead:
    """Update a content block."""
    try:
        item = await content_service.update_content(db, section, slug, payload)
    except ContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ContentRead.model_validate(item)


@router.delete("/content/{section}/{slug}", status_code=204)
async def delete_content(section: str, slug: str, admin: AdminUser, db: Db) -> None:
    """Delete a content block."""
    try:
        await content_service.delete_content(db, section, slug)
    except ContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
