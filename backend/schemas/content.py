"""Content management schemas."""
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class SectionType(StrEnum):
    """Section types for content organization."""

    ABOUTME = "aboutme"
    IHOME = "ihome"
    TRADE4ME = "trade4me"
    SDART = "sdart"


class ContentType(StrEnum):
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
    title: str | None = Field(None, max_length=255)
    body: str | None = None
    data: str | None = None  # JSON string
    order: int = 0
    is_published: bool = True


class ContentCreate(ContentBase):
    """Content creation schema."""

    pass


class ContentUpdate(BaseModel):
    """Content update schema."""

    content_type: ContentType | None = None
    title: str | None = Field(None, max_length=255)
    body: str | None = None
    data: str | None = None
    order: int | None = None
    is_published: bool | None = None


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
    description: str | None = None
    content: str | None = None
    thumbnail_url: HttpUrl | None = None
    project_url: HttpUrl | None = None
    github_url: HttpUrl | None = None
    technologies: str | None = None  # JSON array
    order: int = 0
    is_published: bool = True


class ProjectCreate(ProjectBase):
    """Project creation schema."""

    pass


class ProjectUpdate(BaseModel):
    """Project update schema."""

    section: SectionType | None = None
    title: str | None = Field(None, min_length=1, max_length=255)
    slug: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    content: str | None = None
    thumbnail_url: HttpUrl | None = None
    project_url: HttpUrl | None = None
    github_url: HttpUrl | None = None
    technologies: str | None = None
    order: int | None = None
    is_published: bool | None = None


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
    url: HttpUrl | None = None
    section: SectionType | None = None


class MediaRead(MediaBase):
    """Media read schema."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
