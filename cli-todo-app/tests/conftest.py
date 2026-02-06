"""Shared test fixtures for Todo CLI tests."""

import pytest

from src.models.status import TodoStatus
from src.models.todo import Todo
from src.services.todo_service import TodoService
from src.store.todo_store import TodoStore


@pytest.fixture
def empty_store() -> TodoStore:
    """Create an empty TodoStore for testing."""
    return TodoStore()


@pytest.fixture
def store_with_todos() -> TodoStore:
    """Create a TodoStore with sample todos for testing."""
    store = TodoStore()
    store.add("Buy groceries", "Milk, eggs, bread")
    store.add("Call mom", "")
    store.add("Complete project", "Finish Phase 1")
    # Mark one as complete
    store.mark_complete(2)
    return store


@pytest.fixture
def todo_service(empty_store: TodoStore) -> TodoService:
    """Create a TodoService with empty store for testing."""
    return TodoService(empty_store)


@pytest.fixture
def todo_service_with_data(store_with_todos: TodoStore) -> TodoService:
    """Create a TodoService with sample data for testing."""
    return TodoService(store_with_todos)


@pytest.fixture
def sample_todo() -> Todo:
    """Create a sample Todo for testing."""
    return Todo(
        id=1,
        title="Test Todo",
        description="Test description",
        status=TodoStatus.INCOMPLETE,
    )
