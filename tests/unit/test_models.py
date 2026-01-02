"""Unit tests for models - Todo and TodoStatus."""

from datetime import UTC, datetime

from src.exceptions import (
    EmptyTitleError,
    InvalidIdError,
    TodoError,
    TodoNotFoundError,
    ValidationError,
)
from src.models import Todo, TodoStatus


class TestTodoStatus:
    """Tests for TodoStatus enum."""

    def test_incomplete_value(self) -> None:
        """TodoStatus.INCOMPLETE has value 'incomplete'."""
        assert TodoStatus.INCOMPLETE.value == "incomplete"

    def test_complete_value(self) -> None:
        """TodoStatus.COMPLETE has value 'complete'."""
        assert TodoStatus.COMPLETE.value == "complete"

    def test_str_incomplete(self) -> None:
        """str(TodoStatus.INCOMPLETE) returns 'incomplete'."""
        assert str(TodoStatus.INCOMPLETE) == "incomplete"

    def test_str_complete(self) -> None:
        """str(TodoStatus.COMPLETE) returns 'complete'."""
        assert str(TodoStatus.COMPLETE) == "complete"

    def test_enum_members(self) -> None:
        """TodoStatus has exactly two members."""
        assert len(TodoStatus) == 2
        assert TodoStatus.INCOMPLETE in TodoStatus
        assert TodoStatus.COMPLETE in TodoStatus


class TestTodo:
    """Tests for Todo dataclass."""

    def test_create_todo_with_required_fields(self) -> None:
        """Todo can be created with id and title."""
        todo = Todo(id=1, title="Test Todo")
        assert todo.id == 1
        assert todo.title == "Test Todo"
        assert todo.description == ""
        assert todo.status == TodoStatus.INCOMPLETE

    def test_create_todo_with_all_fields(self) -> None:
        """Todo can be created with all fields."""
        created_at = datetime.now(UTC)
        todo = Todo(
            id=1,
            title="Test Todo",
            description="Test description",
            status=TodoStatus.COMPLETE,
            created_at=created_at,
        )
        assert todo.id == 1
        assert todo.title == "Test Todo"
        assert todo.description == "Test description"
        assert todo.status == TodoStatus.COMPLETE
        assert todo.created_at == created_at

    def test_todo_default_status_is_incomplete(self) -> None:
        """Todo default status is INCOMPLETE."""
        todo = Todo(id=1, title="Test")
        assert todo.status == TodoStatus.INCOMPLETE

    def test_todo_to_dict(self) -> None:
        """Todo.to_dict() returns correct dictionary."""
        todo = Todo(id=1, title="Test", description="Desc")
        result = todo.to_dict()
        assert result["id"] == 1
        assert result["title"] == "Test"
        assert result["description"] == "Desc"
        assert result["status"] == "incomplete"
        assert "created_at" in result

    def test_is_complete_when_incomplete(self) -> None:
        """is_complete() returns False for incomplete todos."""
        todo = Todo(id=1, title="Test", status=TodoStatus.INCOMPLETE)
        assert todo.is_complete() is False

    def test_is_complete_when_complete(self) -> None:
        """is_complete() returns True for complete todos."""
        todo = Todo(id=1, title="Test", status=TodoStatus.COMPLETE)
        assert todo.is_complete() is True


class TestExceptions:
    """Tests for custom exceptions."""

    def test_todo_error_base(self) -> None:
        """TodoError is the base exception with message and code."""
        error = TodoError("Test error", "TEST_CODE")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.code == "TEST_CODE"

    def test_todo_not_found_error(self) -> None:
        """TodoNotFoundError contains the todo ID."""
        error = TodoNotFoundError(42)
        assert error.todo_id == 42
        assert error.message == "Todo with ID 42 not found"
        assert error.code == "TODO_NOT_FOUND"

    def test_validation_error(self) -> None:
        """ValidationError has VALIDATION_ERROR code."""
        error = ValidationError("Invalid input")
        assert error.message == "Invalid input"
        assert error.code == "VALIDATION_ERROR"

    def test_empty_title_error(self) -> None:
        """EmptyTitleError has correct message."""
        error = EmptyTitleError()
        assert error.message == "Title is required"
        assert error.code == "VALIDATION_ERROR"

    def test_invalid_id_error(self) -> None:
        """InvalidIdError has correct message."""
        error = InvalidIdError()
        assert error.message == "Invalid ID. ID must be a positive number"
        assert error.code == "VALIDATION_ERROR"

    def test_exception_inheritance(self) -> None:
        """All exceptions inherit from TodoError."""
        assert issubclass(TodoNotFoundError, TodoError)
        assert issubclass(ValidationError, TodoError)
        assert issubclass(EmptyTitleError, ValidationError)
        assert issubclass(InvalidIdError, ValidationError)
