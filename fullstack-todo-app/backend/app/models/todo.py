"""Todo model definition."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

from app.models.enums import Priority, TodoStatus

if TYPE_CHECKING:
    from app.models.user import User


def _utcnow() -> datetime:
    """Return current UTC time."""
    return datetime.now(timezone.utc)


class Todo(SQLModel, table=True):
    """Todo entity - represents a task item belonging to a user."""

    __tablename__ = "todos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None)
    status: TodoStatus = Field(
        default=TodoStatus.PENDING,
        sa_column=Column(sa.String(20), nullable=False, server_default="pending"),
    )
    priority: Priority = Field(
        default=Priority.MEDIUM,
        sa_column=Column(sa.String(10), nullable=False, server_default="medium"),
    )
    due_date: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
    )
    tags: list[str] = Field(default=[], sa_column=Column(JSONB, default=[]))
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
    user: "User" = Relationship(back_populates="todos")

    @property
    def is_deleted(self) -> bool:
        """Check if todo is soft-deleted."""
        return self.deleted_at is not None

    @property
    def is_overdue(self) -> bool:
        """Check if todo is overdue."""
        if self.due_date is None:
            return False
        return (
            self.due_date < datetime.now(timezone.utc)
            and self.status != TodoStatus.COMPLETED
        )
