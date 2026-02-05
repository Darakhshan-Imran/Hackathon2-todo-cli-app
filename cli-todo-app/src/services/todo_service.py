"""Todo service - business logic layer for todo operations."""

from src.exceptions import ValidationError
from src.models import Todo, TodoStatus
from src.store import TodoStore
from src.utils import validate_id, validate_title


class TodoService:
    """Business logic layer for todo operations.

    This service layer is reusable in Phase 2+ when the storage
    backend changes from in-memory to a database repository.
    """

    def __init__(self, store: TodoStore | None = None) -> None:
        """Initialize the service with a store.

        Args:
            store: The TodoStore to use (creates new one if not provided)
        """
        self._store = store if store is not None else TodoStore()

    def create_todo(self, title: str, description: str = "") -> Todo:
        """Create a new todo.

        Args:
            title: The todo title (required, will be validated)
            description: The todo description (optional)

        Returns:
            The created Todo

        Raises:
            EmptyTitleError: If title is empty
        """
        validated_title = validate_title(title)
        return self._store.add(validated_title, description)

    def get_todo(self, todo_id: int | str) -> Todo:
        """Get a todo by ID.

        Args:
            todo_id: The ID of the todo (will be validated)

        Returns:
            The Todo with the specified ID

        Raises:
            InvalidIdError: If ID is not a valid positive integer
            TodoNotFoundError: If no todo with the ID exists
        """
        validated_id = validate_id(todo_id)
        return self._store.get(validated_id)

    def get_all_todos(self, status_filter: str | None = None) -> list[Todo]:
        """Get all todos, optionally filtered by status.

        Args:
            status_filter: Optional status string ("complete" or "incomplete")

        Returns:
            List of todos
        """
        filter_status: TodoStatus | None = None
        if status_filter is not None:
            if status_filter.lower() == "complete":
                filter_status = TodoStatus.COMPLETE
            elif status_filter.lower() == "incomplete":
                filter_status = TodoStatus.INCOMPLETE
        return self._store.get_all(filter_status)

    def update_todo(
        self,
        todo_id: int | str,
        title: str | None = None,
        description: str | None = None,
    ) -> Todo:
        """Update a todo's title and/or description.

        Args:
            todo_id: The ID of the todo to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated Todo

        Raises:
            InvalidIdError: If ID is not valid
            TodoNotFoundError: If no todo with the ID exists
            ValidationError: If no fields provided or title is empty
        """
        if title is None and description is None:
            raise ValidationError("Specify --title or --description to update")

        validated_id = validate_id(todo_id)

        # Validate title if provided
        validated_title: str | None = None
        if title is not None:
            validated_title = validate_title(title)

        return self._store.update(validated_id, validated_title, description)

    def delete_todo(self, todo_id: int | str) -> None:
        """Delete a todo by ID.

        Args:
            todo_id: The ID of the todo to delete

        Raises:
            InvalidIdError: If ID is not valid
            TodoNotFoundError: If no todo with the ID exists
        """
        validated_id = validate_id(todo_id)
        self._store.delete(validated_id)

    def complete_todo(self, todo_id: int | str) -> Todo:
        """Mark a todo as complete.

        Args:
            todo_id: The ID of the todo to mark complete

        Returns:
            The updated Todo

        Raises:
            InvalidIdError: If ID is not valid
            TodoNotFoundError: If no todo with the ID exists
        """
        validated_id = validate_id(todo_id)
        return self._store.mark_complete(validated_id)

    def incomplete_todo(self, todo_id: int | str) -> Todo:
        """Mark a todo as incomplete.

        Args:
            todo_id: The ID of the todo to mark incomplete

        Returns:
            The updated Todo

        Raises:
            InvalidIdError: If ID is not valid
            TodoNotFoundError: If no todo with the ID exists
        """
        validated_id = validate_id(todo_id)
        return self._store.mark_incomplete(validated_id)

    def count(self) -> int:
        """Return the total number of todos."""
        return self._store.count()
