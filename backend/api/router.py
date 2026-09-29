"""Main API router aggregating v1 sub-routers."""
from fastapi import APIRouter

from backend.api.v1 import admin, content

api_router = APIRouter()
api_router.include_router(content.router, prefix="/v1")
api_router.include_router(admin.router, prefix="/v1")
