"""Content CRUD schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

SECTIONS = ("aboutme", "ihome", "trade4me", "sdart")


class ContentCreate(BaseModel):
    """Payload to create a PageContent block."""

    section: str = Field(min_length=1, max_length=50)
    slug: str = Field(min_length=1, max_length=100, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    title: str = Field(min_length=1, max_length=200)
    body: str = ""
    order: int = 0
    is_published: bool = True


class ContentUpdate(BaseModel):
    """Partial update payload for a PageContent block."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    body: Optional[str] = None
    order: Optional[int] = None
    is_published: Optional[bool] = None


class ContentRead(BaseModel):
    """Serialized PageContent block."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    section: str
    slug: str
    title: str
    body: str
    order: int
    is_published: bool
    created_at: datetime
    updated_at: datetime


class ContentList(BaseModel):
    """List of content blocks for a section."""

    section: str
    items: list[ContentRead]
    total: int
