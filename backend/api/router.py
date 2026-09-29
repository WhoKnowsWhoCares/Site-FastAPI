"""API router configuration."""
from fastapi import APIRouter

from backend.api.v1.admin import router as admin_router
from backend.api.v1.auth import router as auth_router
from backend.api.v1.content import router as content_router


api_router = APIRouter()  # routers carry their own /auth /content /admin prefixes; app mounts at /api
api_router.include_router(auth_router)
api_router.include_router(content_router)
api_router.include_router(admin_router)


__all__ = ["api_router"]