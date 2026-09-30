"""Site-FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import backend.models.content  # noqa: F401

# Import all models to ensure their metadata is registered
import backend.models.user  # noqa: F401
from backend.api.router import api_router
from backend.config import settings
from backend.database import Base, engine

app = FastAPI(
    title="Site-FastAPI",
    description="Personal site with FastAPI backend and Next.js frontend",
    version="0.1.0",
)

# CORS for Next.js dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup() -> None:
    """Create database tables for local sqlite dev only.

    In production the schema is managed by Alembic (`alembic upgrade head`),
    which runs as the container entrypoint before uvicorn starts.
    """
    if settings.database_url.startswith("sqlite://"):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "version": settings.version}


@app.get("/")
async def root() -> dict:
    """Root endpoint - serves the main page."""
    return {
        "message": "Welcome to Site-FastAPI!",
        "api_docs": "/docs",
        "health": "/health"
    }
