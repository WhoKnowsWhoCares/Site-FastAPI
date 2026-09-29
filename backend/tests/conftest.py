"""Test conftest with pytest fixtures."""
import tempfile
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.database import Base, get_db
from backend.models.user import User, OAuthAccount
from backend.models.content import PageContent, Project, Media


# Use a temp file for test database
TEST_DB_PATH = Path(tempfile.mkdtemp()) / "test_site.db"
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB_PATH}"

# Global state - shared across all tests
_engine = None
_session_maker = None


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create test database file and clean up after session."""
    TEST_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    yield
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


@pytest_asyncio.fixture(scope="session")
async def async_engine(setup_test_db):
    """Create a single shared async engine for the entire test session."""
    global _engine, _session_maker
    
    _engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
    )
    _session_maker = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    # Create tables once for the entire session
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield _engine
    
    # Cleanup
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await _engine.dispose()


@pytest_asyncio.fixture
async def test_db(async_engine):
    """Provide a transactional scope for each test."""
    async with _session_maker() as session:
        # Clear all tables before each test
        await session.execute(text("DELETE FROM oauth_accounts"))
        await session.execute(text("DELETE FROM page_content"))
        await session.execute(text("DELETE FROM projects"))
        await session.execute(text("DELETE FROM media"))
        await session.execute(text("DELETE FROM users"))
        await session.commit()
        yield session


@pytest.fixture
def app():
    """Create FastAPI test app."""
    from fastapi import FastAPI
    from backend.api.router import api_router

    application = FastAPI()
    application.include_router(api_router, prefix="/api")
    return application


@pytest_asyncio.fixture
async def client(app, test_db):
    """Create async test client with database override."""
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(test_db):
    """Create a test user."""
    from backend.utils.security import hash_password

    user = User(
        email="test@example.com",
        name="Test User",
        hashed_password=hash_password("testpassword123"),
        is_active=True,
        is_admin=True,
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest_asyncio.fixture
async def admin_token(test_user):
    """Create admin auth token."""
    from backend.utils.security import create_access_token

    token = create_access_token(
        subject=str(test_user.id),
        email=test_user.email,
        is_admin=True,
    )
    return token


@pytest_asyncio.fixture
async def test_content(test_db):
    """Create test content blocks."""
    from backend.models.content import SectionType, ContentType

    contents = []
    for i, section in enumerate([SectionType.ABOUTME, SectionType.IHOME]):
        content = PageContent(
            section=section,
            content_type=ContentType.TEXT,
            title=f"Test Content {i}",
            body="This is test content.",
            order=i,
            is_published=True,
        )
        test_db.add(content)
        contents.append(content)

    await test_db.commit()
    return contents


@pytest_asyncio.fixture
async def test_project(test_db):
    """Create a test project."""
    from backend.models.content import SectionType

    project = Project(
        section=SectionType.ABOUTME,
        title="Test Project",
        slug="test-project",
        description="This is a test project.",
        is_published=True,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)
    return project
