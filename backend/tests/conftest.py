"""Shared pytest fixtures: async in-memory SQLite engine, session, users, tokens."""
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.database import Base
from backend.models.user import User
from backend.services.auth_service import create_access_token, get_password_hash


@pytest.fixture
async def engine():
    eng = create_async_engine("sqlite+aiosqlite://")
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    await eng.dispose()


@pytest.fixture
async def session(engine):
    maker = async_sessionmaker(engine, expire_on_commit=False)
    async with maker() as sess:
        yield sess


@pytest.fixture
async def user(session):
    u = User(
        email="user@example.com",
        name="Regular User",
        hashed_password=get_password_hash("pw"),
        is_active=True,
        is_admin=False,
    )
    session.add(u)
    await session.commit()
    return u


@pytest.fixture
async def admin_user(session):
    u = User(
        email="admin@example.com",
        name="Admin",
        hashed_password=get_password_hash("pw"),
        is_active=True,
        is_admin=True,
    )
    session.add(u)
    await session.commit()
    return u


@pytest.fixture
def token_factory():
    def _make(user_obj):
        return create_access_token({"sub": str(user_obj.id)})

    return _make


@pytest.fixture
async def client(session):
    from fastapi import FastAPI
    from httpx import ASGITransport, AsyncClient

    from backend.api.deps import get_db
    from backend.api.v1.auth import router as auth_router

    app = FastAPI()
    app.include_router(auth_router, prefix="/api/v1")

    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
