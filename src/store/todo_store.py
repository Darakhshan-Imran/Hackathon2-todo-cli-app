"""In-memory todo storage - Phase 1 only, replaced by repository in Phase 2."""

from datetime import UTC, datetime

from src.exceptions import TodoNotFoundError
from src.models import Todo, TodoStatus


class TodoStore:
    """In-memory storage for todos using dict with O(1) lookup.

    This is a Phase 1 implementation. In Phase 2, this will be replaced
    with a repository pattern using SQLAlchemy.
    """

    def __init__(self) -> None:
        """Initialize an empty todo store."""
        self._todos: dict[int, Todo] = {}
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """Generate the next sequential ID."""
        id_value = self._next_id
        self._next_id += 1
        return id_value

    def add(self, title: str, description: str = "") -> Todo:
        """Add a new todo to the store.

        Args:
            title: The todo title (required)
            description: The todo description (optional)

        Returns:
            The created Todo with assigned ID
        """
        todo = Todo(
            id=self._generate_id(),
            title=title,
            description=description,
            status=TodoStatus.INCOMPLETE,
            created_at=datetime.now(UTC),
        )
        self._todos[todo.id] = todo
        return todo

    def get(self, todo_id: int) -> Todo:
        """Get a todo by ID.

        Args:
            todo_id: The ID of the todo to retrieve

        Returns:
            The Todo with the specified ID

        Raises:
            TodoNotFoundError: If no todo with the ID exists
        """
        todo = self._todos.get(todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)
        return todo

    def get_all(self, status_filter: TodoStatus | None = None) -> list[Todo]:
        """Get all todos, optionally filtered by status.

        Args:
            status_filter: Optional status to filter by

        Returns:
            List of todos, sorted by ID
        """
        todos = list(self._todos.values())
        if status_filter is not None:
            todos = [t for t in todos if t.status == status_filter]
        return sorted(todos, key=lambda t: t.id)

    def update(
        self,
        todo_id: int,
        title: str | None = None,
        description: str | None = None,
    ) -> Todo:
        """Update a todo's title and/or description.

        Args:
            todo_id: The ID of the todo to update
            title: New title (if provided)
            description: New description (if provided)

        Returns:
            The updated Todo

        Raises:
            TodoNotFoundError: If no todo with the ID exists
        """
        todo = self.get(todo_id)
        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        return todo

    def delete(self, todo_id: int) -> None:
        """Delete a todo by ID.

        Args:
            todo_id: The ID of the todo to delete

        Raises:
            TodoNotFoundError: If no todo with the ID exists
        """
        if todo_id not in self._todos:
            raise TodoNotFoundError(todo_id)
        del self._todos[todo_id]

    def mark_complete(self, todo_id: int) -> Todo:
        """Mark a todo as complete.

        Args:
            todo_id: The ID of the todo to mark complete

        Returns:
            The updated Todo

        Raises:
            TodoNotFoundError: If no todo with the ID exists
        """
        todo = self.get(todo_id)
        todo.status = TodoStatus.COMPLETE
        return todo

    def mark_incomplete(self, todo_id: int) -> Todo:
        """Mark a todo as incomplete.

        Args:
            todo_id: The ID of the todo to mark incomplete

        Returns:
            The updated Todo

        Raises:
            TodoNotFoundError: If no todo with the ID exists
        """
        todo = self.get(todo_id)
        todo.status = TodoStatus.INCOMPLETE
        return todo

    def count(self) -> int:
        """Return the total number of todos in the store."""
        return len(self._todos)
