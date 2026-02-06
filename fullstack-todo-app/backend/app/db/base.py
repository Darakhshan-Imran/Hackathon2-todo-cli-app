"""SQLModel metadata and base configuration."""

from sqlmodel import SQLModel

# Import all models here to ensure they are registered with SQLModel metadata
# This is required for Alembic migrations to detect all tables
from app.models.todo import Todo  # noqa: F401
from app.models.user import User  # noqa: F401

# Re-export for convenience
__all__ = ["SQLModel", "User", "Todo"]
