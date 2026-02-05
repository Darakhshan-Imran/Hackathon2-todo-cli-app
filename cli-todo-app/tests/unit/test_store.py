"""Unit tests for TodoStore - in-memory storage layer."""

import pytest

from src.exceptions import TodoNotFoundError
from src.models import Todo, TodoStatus
from src.store import TodoStore


class TestTodoStoreInit:
    """Tests for TodoStore initialization."""

    def test_empty_store_on_init(self, empty_store: TodoStore) -> None:
        """New store has no todos."""
        assert empty_store.count() == 0

    def test_get_all_empty_store(self, empty_store: TodoStore) -> None:
        """get_all on empty store returns empty list."""
        assert empty_store.get_all() == []


class TestTodoStoreAdd:
    """Tests for TodoStore.add method."""

    def test_add_returns_todo(self, empty_store: TodoStore) -> None:
        """add() returns a Todo instance."""
        todo = empty_store.add("Test")
        assert isinstance(todo, Todo)

    def test_add_assigns_sequential_ids(self, empty_store: TodoStore) -> None:
        """add() assigns sequential IDs starting from 1."""
        todo1 = empty_store.add("First")
        todo2 = empty_store.add("Second")
        todo3 = empty_store.add("Third")
        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3

    def test_add_sets_title(self, empty_store: TodoStore) -> None:
        """add() sets the title correctly."""
        todo = empty_store.add("Buy groceries")
        assert todo.title == "Buy groceries"

    def test_add_sets_description(self, empty_store: TodoStore) -> None:
        """add() sets the description correctly."""
        todo = empty_store.add("Buy groceries", "Milk, eggs, bread")
        assert todo.description == "Milk, eggs, bread"

    def test_add_default_description_empty(self, empty_store: TodoStore) -> None:
        """add() sets empty description by default."""
        todo = empty_store.add("Test")
        assert todo.description == ""

    def test_add_sets_incomplete_status(self, empty_store: TodoStore) -> None:
        """add() sets status to INCOMPLETE."""
        todo = empty_store.add("Test")
        assert todo.status == TodoStatus.INCOMPLETE

    def test_add_sets_created_at(self, empty_store: TodoStore) -> None:
        """add() sets created_at timestamp."""
        todo = empty_store.add("Test")
        assert todo.created_at is not None

    def test_add_increments_count(self, empty_store: TodoStore) -> None:
        """add() increments the todo count."""
        assert empty_store.count() == 0
        empty_store.add("First")
        assert empty_store.count() == 1
        empty_store.add("Second")
        assert empty_store.count() == 2


class TestTodoStoreGet:
    """Tests for TodoStore.get method."""

    def test_get_existing_todo(self, store_with_todos: TodoStore) -> None:
        """get() returns the correct todo."""
        todo = store_with_todos.get(1)
        assert todo.id == 1
        assert todo.title == "Buy groceries"

    def test_get_nonexistent_todo_raises_error(self, empty_store: TodoStore) -> None:
        """get() raises TodoNotFoundError for nonexistent ID."""
        with pytest.raises(TodoNotFoundError) as exc_info:
            empty_store.get(999)
        assert exc_info.value.todo_id == 999


class TestTodoStoreGetAll:
    """Tests for TodoStore.get_all method."""

    def test_get_all_returns_all_todos(self, store_with_todos: TodoStore) -> None:
        """get_all() returns all todos."""
        todos = store_with_todos.get_all()
        assert len(todos) == 3

    def test_get_all_sorted_by_id(self, store_with_todos: TodoStore) -> None:
        """get_all() returns todos sorted by ID."""
        todos = store_with_todos.get_all()
        ids = [t.id for t in todos]
        assert ids == sorted(ids)

    def test_get_all_filter_complete(self, store_with_todos: TodoStore) -> None:
        """get_all() with COMPLETE filter returns only complete todos."""
        todos = store_with_todos.get_all(TodoStatus.COMPLETE)
        assert len(todos) == 1
        assert all(t.status == TodoStatus.COMPLETE for t in todos)

    def test_get_all_filter_incomplete(self, store_with_todos: TodoStore) -> None:
        """get_all() with INCOMPLETE filter returns only incomplete todos."""
        todos = store_with_todos.get_all(TodoStatus.INCOMPLETE)
        assert len(todos) == 2
        assert all(t.status == TodoStatus.INCOMPLETE for t in todos)


class TestTodoStoreUpdate:
    """Tests for TodoStore.update method."""

    def test_update_title(self, store_with_todos: TodoStore) -> None:
        """update() changes the title."""
        todo = store_with_todos.update(1, title="New title")
        assert todo.title == "New title"

    def test_update_description(self, store_with_todos: TodoStore) -> None:
        """update() changes the description."""
        todo = store_with_todos.update(1, description="New description")
        assert todo.description == "New description"

    def test_update_both_fields(self, store_with_todos: TodoStore) -> None:
        """update() can change both title and description."""
        todo = store_with_todos.update(1, title="New", description="Desc")
        assert todo.title == "New"
        assert todo.description == "Desc"

    def test_update_preserves_other_fields(self, store_with_todos: TodoStore) -> None:
        """update() preserves unchanged fields."""
        original = store_with_todos.get(1)
        original_status = original.status
        original_created = original.created_at

        updated = store_with_todos.update(1, title="Changed")
        assert updated.status == original_status
        assert updated.created_at == original_created

    def test_update_nonexistent_raises_error(self, empty_store: TodoStore) -> None:
        """update() raises TodoNotFoundError for nonexistent ID."""
        with pytest.raises(TodoNotFoundError):
            empty_store.update(999, title="Test")


class TestTodoStoreDelete:
    """Tests for TodoStore.delete method."""

    def test_delete_removes_todo(self, store_with_todos: TodoStore) -> None:
        """delete() removes the todo from the store."""
        initial_count = store_with_todos.count()
        store_with_todos.delete(1)
        assert store_with_todos.count() == initial_count - 1

    def test_delete_todo_not_retrievable(self, store_with_todos: TodoStore) -> None:
        """delete() makes the todo not retrievable."""
        store_with_todos.delete(1)
        with pytest.raises(TodoNotFoundError):
            store_with_todos.get(1)

    def test_delete_nonexistent_raises_error(self, empty_store: TodoStore) -> None:
        """delete() raises TodoNotFoundError for nonexistent ID."""
        with pytest.raises(TodoNotFoundError):
            empty_store.delete(999)


class TestTodoStoreMarkComplete:
    """Tests for TodoStore.mark_complete method."""

    def test_mark_complete_changes_status(self, store_with_todos: TodoStore) -> None:
        """mark_complete() sets status to COMPLETE."""
        todo = store_with_todos.mark_complete(1)
        assert todo.status == TodoStatus.COMPLETE

    def test_mark_complete_returns_todo(self, store_with_todos: TodoStore) -> None:
        """mark_complete() returns the updated todo."""
        todo = store_with_todos.mark_complete(1)
        assert isinstance(todo, Todo)
        assert todo.id == 1

    def test_mark_complete_nonexistent_raises_error(
        self, empty_store: TodoStore
    ) -> None:
        """mark_complete() raises TodoNotFoundError for nonexistent ID."""
        with pytest.raises(TodoNotFoundError):
            empty_store.mark_complete(999)


class TestTodoStoreMarkIncomplete:
    """Tests for TodoStore.mark_incomplete method."""

    def test_mark_incomplete_changes_status(self, store_with_todos: TodoStore) -> None:
        """mark_incomplete() sets status to INCOMPLETE."""
        # First mark as complete
        store_with_todos.mark_complete(1)
        # Then mark as incomplete
        todo = store_with_todos.mark_incomplete(1)
        assert todo.status == TodoStatus.INCOMPLETE

    def test_mark_incomplete_returns_todo(self, store_with_todos: TodoStore) -> None:
        """mark_incomplete() returns the updated todo."""
        todo = store_with_todos.mark_incomplete(2)  # ID 2 is already complete
        assert isinstance(todo, Todo)
        assert todo.id == 2

    def test_mark_incomplete_nonexistent_raises_error(
        self, empty_store: TodoStore
    ) -> None:
        """mark_incomplete() raises TodoNotFoundError for nonexistent ID."""
        with pytest.raises(TodoNotFoundError):
            empty_store.mark_incomplete(999)


class TestTodoStoreCount:
    """Tests for TodoStore.count method."""

    def test_count_empty_store(self, empty_store: TodoStore) -> None:
        """count() returns 0 for empty store."""
        assert empty_store.count() == 0

    def test_count_with_todos(self, store_with_todos: TodoStore) -> None:
        """count() returns correct number of todos."""
        assert store_with_todos.count() == 3
