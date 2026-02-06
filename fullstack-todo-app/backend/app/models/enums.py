"""Enum definitions for Todo status and priority."""

from enum import Enum


class FlexibleEnum(str, Enum):
    """Base enum that normalizes input: strips, lowercases, and replaces hyphens/spaces with underscores."""

    @classmethod
    def _missing_(cls, value: object) -> "FlexibleEnum | None":
        if not isinstance(value, str):
            return None
        normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
        for member in cls:
            if member.value == normalized:
                return member
        return None


class TodoStatus(FlexibleEnum):
    """Todo item status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Priority(FlexibleEnum):
    """Todo item priority level."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
