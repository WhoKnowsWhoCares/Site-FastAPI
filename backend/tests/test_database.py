"""Tests for database configuration."""
from sqlalchemy.ext.asyncio import AsyncEngine

from backend.database import engine, Base, async_session_maker


def test_engine_exists():
    """Test that async engine is created."""
    assert engine is not None
    assert isinstance(engine, AsyncEngine)


def test_engine_url():
    """Test that engine has correct URL (aiosqlite for async)."""
    assert "sqlite+aiosqlite" in str(engine.url) or "sqlite" in str(engine.url)


def test_base_class_exists():
    """Test that Base declarative class is available."""
    assert Base is not None
    assert hasattr(Base, "metadata")


def test_session_maker_exists():
    """Test that async session maker is configured."""
    assert async_session_maker is not None
