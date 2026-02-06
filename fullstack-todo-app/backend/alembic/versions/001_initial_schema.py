"""Initial schema for users and todos tables.

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-02-06

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create users and todos tables with indexes."""
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create unique indexes for users
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    # Create index for soft delete queries
    op.create_index(
        "ix_users_deleted_at",
        "users",
        ["deleted_at"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )

    # Create todos table
    op.create_table(
        "todos",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default="pending",
            nullable=False,
        ),
        sa.Column(
            "priority",
            sa.String(length=10),
            server_default="medium",
            nullable=False,
        ),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "tags",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default="[]",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes for todos
    # Index for user's todos (most common query pattern)
    op.create_index("ix_todos_user_id", "todos", ["user_id"])

    # Composite index for user's active todos (user_id + deleted_at)
    op.create_index(
        "ix_todos_user_active",
        "todos",
        ["user_id", "deleted_at"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )

    # Index for filtering by status
    op.create_index("ix_todos_status", "todos", ["status"])

    # Index for filtering by priority
    op.create_index("ix_todos_priority", "todos", ["priority"])

    # Index for due date sorting/filtering
    op.create_index("ix_todos_due_date", "todos", ["due_date"])

    # Composite index for common query: user's todos filtered by status
    op.create_index(
        "ix_todos_user_status",
        "todos",
        ["user_id", "status"],
    )

    # Index for created_at sorting
    op.create_index("ix_todos_created_at", "todos", ["created_at"])

    # GIN index for JSONB tags (for tag-based queries)
    op.create_index(
        "ix_todos_tags",
        "todos",
        ["tags"],
        postgresql_using="gin",
    )


def downgrade() -> None:
    """Drop todos and users tables."""
    # Drop todos indexes
    op.drop_index("ix_todos_tags", table_name="todos")
    op.drop_index("ix_todos_created_at", table_name="todos")
    op.drop_index("ix_todos_user_status", table_name="todos")
    op.drop_index("ix_todos_due_date", table_name="todos")
    op.drop_index("ix_todos_priority", table_name="todos")
    op.drop_index("ix_todos_status", table_name="todos")
    op.drop_index("ix_todos_user_active", table_name="todos")
    op.drop_index("ix_todos_user_id", table_name="todos")

    # Drop todos table
    op.drop_table("todos")

    # Drop users indexes
    op.drop_index("ix_users_deleted_at", table_name="users")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_email", table_name="users")

    # Drop users table
    op.drop_table("users")
