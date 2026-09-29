"""Common schemas for pagination and error responses."""
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination query parameters."""

    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""

    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    """Error response schema."""

    detail: str
    error_code: Optional[str] = None
    status_code: int


class SuccessResponse(BaseModel):
    """Generic success response."""

    message: str
    data: Optional[dict] = None


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str
    version: str