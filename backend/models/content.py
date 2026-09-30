"""Content models for pages, projects, and media."""
from enum import StrEnum

import sqlalchemy as sa
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin


def _enum_column(enum_cls: type[StrEnum]) -> sa.Enum:
    """VARCHAR-backed enum (matches migrations) storing StrEnum values."""
    return sa.Enum(
        enum_cls,
        values_callable=lambda e: [m.value for m in e],
        native_enum=False,
    )


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


class PageContent(Base, TimestampMixin):
    """Page content blocks for each section."""

    __tablename__ = "page_content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    section: Mapped[SectionType] = mapped_column(
        _enum_column(SectionType),
        nullable=False,
        index=True,
    )
    content_type: Mapped[ContentType] = mapped_column(
        _enum_column(ContentType),
        nullable=False,
    )
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    data: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON for flexible content
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_published: Mapped[bool] = mapped_column(default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<PageContent(section={self.section}, type={self.content_type}, order={self.order})>"


class Project(Base, TimestampMixin):
    """Project showcase model."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    section: Mapped[SectionType] = mapped_column(
        _enum_column(SectionType),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)  # Full project content (markdown/HTML)
    thumbnail_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    project_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    github_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    technologies: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON array
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_published: Mapped[bool] = mapped_column(default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Project(section={self.section}, slug={self.slug})>"


class Media(Base, TimestampMixin):
    """Media files (images, documents)."""

    __tablename__ = "media"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    path: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    section: Mapped[SectionType | None] = mapped_column(
        _enum_column(SectionType),
        nullable=True,
        index=True,
    )

    def __repr__(self) -> str:
        return f"<Media(filename={self.filename}, type={self.content_type})>"
