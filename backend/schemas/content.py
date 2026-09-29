"""Content management schemas."""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class SectionType(str, Enum):
    """Section types for content organization."""

    ABOUTME = "aboutme"
    IHOME = "ihome"
    TRADE4ME = "trade4me"
    SDART = "sdart"


class ContentType(str, Enum):
    """Content block types."""

    HERO = "hero"
    TEXT = "text"
    IMAGE = "image"
    GALLERY = "gallery"
    CARD = "card"
    LIST = "list"
    METRIC = "metric"
    CHART = "chart"


class ContentBase(BaseModel):
    """Base content schema."""

    section: SectionType
    content_type: ContentType
    title: Optional[str] = Field(None, max_length=255)
    body: Optional[str] = None
    data: Optional[str] = None  # JSON string
    order: int = 0
    is_published: bool = True


class ContentCreate(ContentBase):
    """Content creation schema."""

    pass


class ContentUpdate(BaseModel):
    """Content update schema."""

    content_type: Optional[ContentType] = None
    title: Optional[str] = Field(None, max_length=255)
    body: Optional[str] = None
    data: Optional[str] = None
    order: Optional[int] = None
    is_published: Optional[bool] = None


class ContentRead(ContentBase):
    """Content read schema."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContentList(BaseModel):
    """Paginated content list."""

    items: list[ContentRead]
    total: int
    page: int
    page_size: int
    total_pages: int


class ProjectBase(BaseModel):
    """Base project schema."""

    section: SectionType
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    content: Optional[str] = None
    thumbnail_url: Optional[HttpUrl] = None
    project_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    technologies: Optional[str] = None  # JSON array
    order: int = 0
    is_published: bool = True


class ProjectCreate(ProjectBase):
    """Project creation schema."""

    pass


class ProjectUpdate(BaseModel):
    """Project update schema."""

    section: Optional[SectionType] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    content: Optional[str] = None
    thumbnail_url: Optional[HttpUrl] = None
    project_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    technologies: Optional[str] = None
    order: Optional[int] = None
    is_published: Optional[bool] = None


class ProjectRead(ProjectBase):
    """Project read schema."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MediaBase(BaseModel):
    """Base media schema."""

    filename: str
    original_filename: str
    content_type: str
    size: int
    path: str
    url: Optional[HttpUrl] = None
    section: Optional[SectionType] = None


class MediaRead(MediaBase):
    """Media read schema."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)