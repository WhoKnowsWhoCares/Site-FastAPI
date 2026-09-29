"""Main API router."""
from fastapi import APIRouter

from backend.api.v1 import auth

api_router = APIRouter()
api_router.include_router(auth.router)
