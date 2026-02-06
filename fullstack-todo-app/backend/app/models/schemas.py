"""Pydantic request/response schemas."""

from datetime import datetime, timezone
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.enums import Priority, TodoStatus


def _normalize_enum_value(v: str | None) -> str | None:
    """Normalize enum input: strip, lowercase, replace hyphens/spaces with underscores."""
    if v is None or not isinstance(v, str):
        return v
    return v.strip().lower().replace("-", "_").replace(" ", "_")

T = TypeVar("T")


# ============================================================================
# API Response Wrappers
# ============================================================================


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    success: bool
    data: T | None = None
    error: str | None = None
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


class PaginatedData(BaseModel, Generic[T]):
    """Paginated data wrapper."""

    items: list[T]
    page: int
    per_page: int
    total: int
    total_pages: int


# ============================================================================
# Auth Schemas
# ============================================================================


class SignupRequest(BaseModel):
    """User registration request."""

    email: EmailStr
    username: str = Field(
        min_length=3,
        max_length=30,
        pattern=r"^[a-zA-Z0-9_]+$",
    )
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    """User login request."""

    email: EmailStr
    password: str


class TokenData(BaseModel):
    """Token response data."""

    access_token: str
    token_type: str = "bearer"


# ============================================================================
# User Schemas
# ============================================================================


class UserResponse(BaseModel):
    """User profile response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    username: str
    created_at: datetime


class UserUpdate(BaseModel):
    """User profile update request."""

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=30,
        pattern=r"^[a-zA-Z0-9_]+$",
    )


# ============================================================================
# Todo Schemas
# ============================================================================


class TodoCreate(BaseModel):
    """Todo creation request."""

    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: TodoStatus = TodoStatus.PENDING
    priority: Priority = Priority.MEDIUM
    due_date: datetime | None = None

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, v: str | None) -> str | None:
        return _normalize_enum_value(v)

    @field_validator("priority", mode="before")
    @classmethod
    def normalize_priority(cls, v: str | None) -> str | None:
        return _normalize_enum_value(v)


class TodoResponse(BaseModel):
    """Todo response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: TodoStatus
    priority: Priority
    due_date: datetime | None
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class TodoUpdate(BaseModel):
    """Todo update request - all fields optional."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: TodoStatus | None = None
    priority: Priority | None = None
    due_date: datetime | None = None

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, v: str | None) -> str | None:
        return _normalize_enum_value(v)

    @field_validator("priority", mode="before")
    @classmethod
    def normalize_priority(cls, v: str | None) -> str | None:
        return _normalize_enum_value(v)


class TodoListParams(BaseModel):
    """Todo list query parameters."""

    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
    status: TodoStatus | None = None
    priority: Priority | None = None
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", pattern=r"^(asc|desc)$")
