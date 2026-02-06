"""Unit tests for TodoService - business logic layer."""

import pytest

from src.exceptions import (
    EmptyTitleError,
    InvalidIdError,
    TodoNotFoundError,
    ValidationError,
)
from src.models import Todo, TodoStatus
from src.services import TodoService
from src.store import TodoStore


class TestTodoServiceInit:
    """Tests for TodoService initialization."""

    def test_creates_default_store(self) -> None:
        """TodoService creates a default store if none provided."""
        service = TodoService()
        assert service.count() == 0

    def test_uses_provided_store(self, empty_store: TodoStore) -> None:
        """TodoService uses the provided store."""
        empty_store.add("Pre-existing todo")
        service = TodoService(empty_store)
        assert service.count() == 1


class TestTodoServiceCreateTodo:
    """Tests for TodoService.create_todo method."""

    def test_create_returns_todo(self, todo_service: TodoService) -> None:
        """create_todo() returns a Todo instance."""
        todo = todo_service.create_todo("Test")
        assert isinstance(todo, Todo)

    def test_create_sets_title(self, todo_service: TodoService) -> None:
        """create_todo() sets the title."""
        todo = todo_service.create_todo("Buy groceries")
        assert todo.title == "Buy groceries"

    def test_create_sets_description(self, todo_service: TodoService) -> None:
        """create_todo() sets the description."""
        todo = todo_service.create_todo("Buy groceries", "Milk, eggs")
        assert todo.description == "Milk, eggs"

    def test_create_validates_title(self, todo_service: TodoService) -> None:
        """create_todo() validates and strips the title."""
        todo = todo_service.create_todo("  Padded title  ")
        assert todo.title == "Padded title"

    def test_create_empty_title_raises_error(self, todo_service: TodoService) -> None:
        """create_todo() raises EmptyTitleError for empty title."""
        with pytest.raises(EmptyTitleError):
            todo_service.create_todo("")

    def test_create_whitespace_title_raises_error(
        self, todo_service: TodoService
    ) -> None:
        """create_todo() raises EmptyTitleError for whitespace-only title."""
        with pytest.raises(EmptyTitleError):
            todo_service.create_todo("   ")


class TestTodoServiceGetTodo:
    """Tests for TodoService.get_todo method."""

    def test_get_existing_todo(self, todo_service: TodoService) -> None:
        """get_todo() returns the correct todo."""
        created = todo_service.create_todo("Test")
        retrieved = todo_service.get_todo(created.id)
        assert retrieved.id == created.id
        assert retrieved.title == created.title

    def test_get_with_string_id(self, todo_service: TodoService) -> None:
        """get_todo() accepts string ID."""
        created = todo_service.create_todo("Test")
        retrieved = todo_service.get_todo(str(created.id))
        assert retrieved.id == created.id

    def test_get_nonexistent_raises_error(self, todo_service: TodoService) -> None:
        """get_todo() raises TodoNotFoundError for nonexistent ID."""
        with pytest.raises(TodoNotFoundError):
            todo_service.get_todo(999)

    def test_get_invalid_id_raises_error(self, todo_service: TodoService) -> None:
        """get_todo() raises InvalidIdError for invalid ID."""
        with pytest.raises(InvalidIdError):
            todo_service.get_todo("abc")

    def test_get_negative_id_raises_error(self, todo_service: TodoService) -> None:
        """get_todo() raises InvalidIdError for negative ID."""
        with pytest.raises(InvalidIdError):
            todo_service.get_todo(-1)


class TestTodoServiceGetAllTodos:
    """Tests for TodoService.get_all_todos method."""

    def test_get_all_empty(self, todo_service: TodoService) -> None:
        """get_all_todos() returns empty list when no todos."""
        assert todo_service.get_all_todos() == []

    def test_get_all_returns_all(self, todo_service: TodoService) -> None:
        """get_all_todos() returns all todos."""
        todo_service.create_todo("First")
        todo_service.create_todo("Second")
        todos = todo_service.get_all_todos()
        assert len(todos) == 2

    def test_get_all_filter_complete(self, todo_service: TodoService) -> None:
        """get_all_todos() filters by 'complete' status."""
        todo1 = todo_service.create_todo("One")
        todo_service.create_todo("Two")
        todo_service.complete_todo(todo1.id)

        todos = todo_service.get_all_todos("complete")
        assert len(todos) == 1
        assert todos[0].status == TodoStatus.COMPLETE

    def test_get_all_filter_incomplete(self, todo_service: TodoService) -> None:
        """get_all_todos() filters by 'incomplete' status."""
        todo1 = todo_service.create_todo("One")
        todo_service.create_todo("Two")
        todo_service.complete_todo(todo1.id)

        todos = todo_service.get_all_todos("incomplete")
        assert len(todos) == 1
        assert todos[0].status == TodoStatus.INCOMPLETE

    def test_get_all_filter_case_insensitive(self, todo_service: TodoService) -> None:
        """get_all_todos() filter is case insensitive."""
        todo1 = todo_service.create_todo("One")
        todo_service.complete_todo(todo1.id)

        todos = todo_service.get_all_todos("COMPLETE")
        assert len(todos) == 1


class TestTodoServiceUpdateTodo:
    """Tests for TodoService.update_todo method."""

    def test_update_title(self, todo_service: TodoService) -> None:
        """update_todo() updates the title."""
        created = todo_service.create_todo("Original")
        updated = todo_service.update_todo(created.id, title="Updated")
        assert updated.title == "Updated"

    def test_update_description(self, todo_service: TodoService) -> None:
        """update_todo() updates the description."""
        created = todo_service.create_todo("Test", "Original")
        updated = todo_service.update_todo(created.id, description="Updated desc")
        assert updated.description == "Updated desc"

    def test_update_both_fields(self, todo_service: TodoService) -> None:
        """update_todo() can update both title and description."""
        created = todo_service.create_todo("Original", "Old desc")
        updated = todo_service.update_todo(
            created.id, title="New", description="New desc"
        )
        assert updated.title == "New"
        assert updated.description == "New desc"

    def test_update_with_string_id(self, todo_service: TodoService) -> None:
        """update_todo() accepts string ID."""
        created = todo_service.create_todo("Test")
        updated = todo_service.update_todo(str(created.id), title="Updated")
        assert updated.title == "Updated"

    def test_update_no_fields_raises_error(self, todo_service: TodoService) -> None:
        """update_todo() raises ValidationError when no fields provided."""
        created = todo_service.create_todo("Test")
        with pytest.raises(ValidationError):
            todo_service.update_todo(created.id)

    def test_update_empty_title_raises_error(self, todo_service: TodoService) -> None:
        """update_todo() raises EmptyTitleError for empty title."""
        created = todo_service.create_todo("Test")
        with pytest.raises(EmptyTitleError):
            todo_service.update_todo(created.id, title="")

    def test_update_nonexistent_raises_error(self, todo_service: TodoService) -> None:
        """update_todo() raises TodoNotFoundError for nonexistent ID."""
        with pytest.raises(TodoNotFoundError):
            todo_service.update_todo(999, title="Test")

    def test_update_invalid_id_raises_error(self, todo_service: TodoService) -> None:
        """update_todo() raises InvalidIdError for invalid ID."""
        with pytest.raises(InvalidIdError):
            todo_service.update_todo("abc", title="Test")


class TestTodoServiceDeleteTodo:
    """Tests for TodoService.delete_todo method."""

    def test_delete_removes_todo(self, todo_service: TodoService) -> None:
        """delete_todo() removes the todo."""
        created = todo_service.create_todo("Test")
        todo_service.delete_todo(created.id)
        assert todo_service.count() == 0

    def test_delete_with_string_id(self, todo_service: TodoService) -> None:
        """delete_todo() accepts string ID."""
        created = todo_service.create_todo("Test")
        todo_service.delete_todo(str(created.id))
        assert todo_service.count() == 0

    def test_delete_nonexistent_raises_error(self, todo_service: TodoService) -> None:
        """delete_todo() raises TodoNotFoundError for nonexistent ID."""
        with pytest.raises(TodoNotFoundError):
            todo_service.delete_todo(999)

    def test_delete_invalid_id_raises_error(self, todo_service: TodoService) -> None:
        """delete_todo() raises InvalidIdError for invalid ID."""
        with pytest.raises(InvalidIdError):
            todo_service.delete_todo("abc")


class TestTodoServiceCompleteTodo:
    """Tests for TodoService.complete_todo method."""

    def test_complete_sets_status(self, todo_service: TodoService) -> None:
        """complete_todo() sets status to COMPLETE."""
        created = todo_service.create_todo("Test")
        completed = todo_service.complete_todo(created.id)
        assert completed.status == TodoStatus.COMPLETE

    def test_complete_with_string_id(self, todo_service: TodoService) -> None:
        """complete_todo() accepts string ID."""
        created = todo_service.create_todo("Test")
        completed = todo_service.complete_todo(str(created.id))
        assert completed.status == TodoStatus.COMPLETE

    def test_complete_nonexistent_raises_error(self, todo_service: TodoService) -> None:
        """complete_todo() raises TodoNotFoundError for nonexistent ID."""
        with pytest.raises(TodoNotFoundError):
            todo_service.complete_todo(999)

    def test_complete_invalid_id_raises_error(self, todo_service: TodoService) -> None:
        """complete_todo() raises InvalidIdError for invalid ID."""
        with pytest.raises(InvalidIdError):
            todo_service.complete_todo("abc")


class TestTodoServiceIncompleteTodo:
    """Tests for TodoService.incomplete_todo method."""

    def test_incomplete_sets_status(self, todo_service: TodoService) -> None:
        """incomplete_todo() sets status to INCOMPLETE."""
        created = todo_service.create_todo("Test")
        todo_service.complete_todo(created.id)
        incomplete = todo_service.incomplete_todo(created.id)
        assert incomplete.status == TodoStatus.INCOMPLETE

    def test_incomplete_with_string_id(self, todo_service: TodoService) -> None:
        """incomplete_todo() accepts string ID."""
        created = todo_service.create_todo("Test")
        todo_service.complete_todo(created.id)
        incomplete = todo_service.incomplete_todo(str(created.id))
        assert incomplete.status == TodoStatus.INCOMPLETE

    def test_incomplete_nonexistent_raises_error(
        self, todo_service: TodoService
    ) -> None:
        """incomplete_todo() raises TodoNotFoundError for nonexistent ID."""
        with pytest.raises(TodoNotFoundError):
            todo_service.incomplete_todo(999)

    def test_incomplete_invalid_id_raises_error(
        self, todo_service: TodoService
    ) -> None:
        """incomplete_todo() raises InvalidIdError for invalid ID."""
        with pytest.raises(InvalidIdError):
            todo_service.incomplete_todo("abc")


class TestTodoServiceCount:
    """Tests for TodoService.count method."""

    def test_count_empty(self, todo_service: TodoService) -> None:
        """count() returns 0 for empty service."""
        assert todo_service.count() == 0

    def test_count_with_todos(self, todo_service: TodoService) -> None:
        """count() returns correct count."""
        todo_service.create_todo("One")
        todo_service.create_todo("Two")
        assert todo_service.count() == 2
