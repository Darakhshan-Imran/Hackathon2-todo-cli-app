"""Todo dataclass - represents a task to be completed."""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from src.models.status import TodoStatus


@dataclass
class Todo:
    """A task to be completed.

    Attributes:
        id: Unique positive integer identifier (auto-assigned, immutable)
        title: Brief description of the task (required, 1-200 characters)
        description: Detailed information about the task (optional)
        status: Completion state (default: INCOMPLETE)
        created_at: Timestamp when todo was created (auto-assigned)
    """

    id: int
    title: str
    description: str = ""
    status: TodoStatus = TodoStatus.INCOMPLETE
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, str | int]:
        """Convert todo to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": str(self.status),
            "created_at": self.created_at.isoformat(),
        }

    def is_complete(self) -> bool:
        """Check if the todo is marked as complete."""
        return self.status == TodoStatus.COMPLETE
