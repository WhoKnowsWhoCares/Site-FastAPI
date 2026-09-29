"""Content models: PageContent, Project, Media."""
from typing import Optional

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base
from backend.models.base import TimestampMixin


class PageContent(Base, TimestampMixin):
    """Content block for a site section (aboutme, ihome, trade4me, sdart)."""

    __tablename__ = "page_contents"

    id: Mapped[int] = mapped_column(primary_key=True)
    section: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, default="", nullable=False)
    order: Mapped[int] = mapped_column(default=0, nullable=False)
    is_published: Mapped[bool] = mapped_column(default=True, nullable=False)

    __table_args__ = (
        # unique constraint is enforced at service level for clarity in tests
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<PageContent {self.section}/{self.slug}>"


class Project(Base, TimestampMixin):
    """Portfolio project entry."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    section: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    order: Mapped[int] = mapped_column(default=0, nullable=False)
    is_published: Mapped[bool] = mapped_column(default=True, nullable=False)

    media: Mapped[list["Media"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Project {self.name}>"


class Media(Base, TimestampMixin):
    """Media item (image/video url) attached to a project."""

    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=True, index=True
    )
    kind: Mapped[str] = mapped_column(String(20), default="image", nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    alt: Mapped[str] = mapped_column(String(300), default="", nullable=False)
    order: Mapped[int] = mapped_column(default=0, nullable=False)

    project: Mapped[Optional["Project"]] = relationship(back_populates="media")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Media {self.kind}:{self.url}>"
