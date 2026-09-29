"""Site-FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.api.router import api_router
from backend.config import settings
from backend.database import engine, Base


# Import all models to ensure their metadata is registered
import backend.models.user  # noqa: F401
import backend.models.content  # noqa: F401


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
async def startup():
    """Create database tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": settings.version}


@app.get("/")
async def root():
    """Root endpoint - serves the main page."""
    return {
        "message": "Welcome to Site-FastAPI!",
        "api_docs": "/docs",
        "health": "/health"
    }
