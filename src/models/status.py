"""TodoStatus enum - represents the completion state of a todo."""

from enum import Enum


class TodoStatus(Enum):
    """Completion state of a todo item."""

    INCOMPLETE = "incomplete"
    COMPLETE = "complete"

    def __str__(self) -> str:
        """Return the string value of the status."""
        return self.value
