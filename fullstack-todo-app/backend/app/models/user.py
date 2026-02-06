"""User model definition."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.todo import Todo


def _utcnow() -> datetime:
    """Return current UTC time."""
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    """User entity - represents an authenticated account holder."""

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    username: str = Field(max_length=30, unique=True, index=True)
    password_hash: str = Field()
    created_at: datetime = Field(
        default_factory=_utcnow,
        sa_type=sa.DateTime(timezone=True),
    )
    updated_at: datetime = Field(
        default_factory=_utcnow,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"onupdate": _utcnow},
    )
    deleted_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
    )

    # Relationships
    todos: list["Todo"] = Relationship(back_populates="user")

    @property
    def is_deleted(self) -> bool:
        """Check if user is soft-deleted."""
        return self.deleted_at is not None
