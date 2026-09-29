"""Site-FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import models  # noqa: F401  (import registers models on Base)
from backend.api.router import api_router
from backend.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
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
        "health": "/health",
    }
