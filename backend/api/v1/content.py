"""Public content endpoints: /api/v1/content/*."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas.content import ContentList, ContentRead
from backend.services import content_service
from backend.services.content_service import ContentNotFoundError

router = APIRouter(prefix="/content", tags=["content"])

VALID_SECTIONS = ("aboutme", "ihome", "trade4me", "sdart")

Db = Annotated[AsyncSession, Depends(get_db)]


def _ensure_valid_section(section: str) -> None:
    if section not in VALID_SECTIONS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown section: {section}",
        )


@router.get("/{section}", response_model=ContentList)
async def get_section_content(section: str, db: Db) -> ContentList:
    """Return published content blocks for a section."""
    _ensure_valid_section(section)
    items = await content_service.list_content(db, section)
    total = await content_service.count_content(db, section)
    return ContentList(
        section=section,
        items=[ContentRead.model_validate(i) for i in items],
        total=total,
    )


@router.get("/{section}/{slug}", response_model=ContentRead)
async def get_content_item(section: str, slug: str, db: Db) -> ContentRead:
    """Return a single published content block by section and slug."""
    _ensure_valid_section(section)
    try:
        item = await content_service.get_content(db, section, slug)
    except ContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ContentRead.model_validate(item)
