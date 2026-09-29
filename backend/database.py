"""Async database engine and session factory."""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from backend.config import settings


class Base(DeclarativeBase):
    """Declarative base used by all models."""


def make_engine(database_url: str):
    """Create an async engine for the given URL."""
    return create_async_engine(database_url, echo=False)


def make_session_factory(engine) -> async_sessionmaker[AsyncSession]:
    """Create a session factory bound to the engine."""
    return async_sessionmaker(engine, expire_on_commit=False)


# Default engine for the running app (sync sqlite URL converted to aiosqlite)
_database_url = settings.DATABASE_URL
if _database_url.startswith("sqlite:///"):
    _database_url = _database_url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)

engine = make_engine(_database_url)
SessionLocal = make_session_factory(engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding a database session."""
    async with SessionLocal() as session:
        yield session
