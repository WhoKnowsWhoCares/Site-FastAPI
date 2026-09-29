"""Auth-related Pydantic schemas."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OAuthCallback(BaseModel):
    code: str
    state: str | None = None


class OAuthUrlResponse(BaseModel):
    provider: str
    url: str
    state: str
