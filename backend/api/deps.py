"""Shared API dependencies."""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db

bearer_scheme = HTTPBearer(auto_error=False)

# Admin authentication token. In the full auth flow this is a JWT; for now the
# admin API accepts a bearer token equal to settings.ADMIN_TOKEN.
DEFAULT_ADMIN_TOKEN = "admin-test-token"


async def get_current_admin(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> str:
    """Require a valid admin bearer token; return the admin identity."""
    from backend.config import settings

    expected = getattr(settings, "ADMIN_TOKEN", None) or DEFAULT_ADMIN_TOKEN
    if credentials is None or credentials.credentials != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return "admin"


DbSession = Annotated[AsyncSession, Depends(get_db)]
Db = DbSession  # short alias
AdminUser = Annotated[str, Depends(get_current_admin)]
