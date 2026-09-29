"""Site-FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.api.router import api_router
from backend.config import settings
from backend.database import engine, Base
from backend.models import user  # noqa: F401 — register models before create_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Site-FastAPI",
    description="Personal site with FastAPI backend and Next.js frontend",
    version="0.1.0",
    lifespan=lifespan,
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

# Serve Next.js static files in production
frontend_dist = Path(__file__).parent.parent / "frontend" / ".next" / "standalone"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}


@app.get("/")
async def root():
    """Root endpoint - serves the main page."""
    return {
        "message": "Welcome to Site-FastAPI!",
        "api_docs": "/docs",
        "health": "/health"
    }
