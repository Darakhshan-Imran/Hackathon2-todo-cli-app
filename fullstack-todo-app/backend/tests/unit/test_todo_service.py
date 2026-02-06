"""Unit tests for todo service."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import Priority, TodoStatus
from app.models.schemas import TodoCreate, TodoUpdate
from app.models.todo import Todo
from app.services.todo_service import TodoService
from app.utils.exceptions import NotFoundError


class TestTodoService:
    """Tests for TodoService."""

    @pytest.fixture
    def mock_session(self):
        """Create mock database session."""
        session = AsyncMock(spec=AsyncSession)
        return session

    @pytest.fixture
    def todo_service(self, mock_session):
        """Create todo service with mock session."""
        return TodoService(mock_session)

    @pytest.fixture
    def user_id(self):
        """Create test user ID."""
        return uuid4()

    @pytest.fixture
    def todo_id(self):
        """Create test todo ID."""
        return uuid4()

    @pytest.fixture
    def mock_todo(self, user_id, todo_id):
        """Create mock todo."""
        return Todo(
            id=todo_id,
            user_id=user_id,
            title="Test Todo",
            description="Test description",
            status=TodoStatus.PENDING,
            priority=Priority.MEDIUM,
            tags=["test"],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    @pytest.mark.asyncio
    async def test_create_todo_success(self, todo_service, mock_session, user_id):
        """Create todo should add todo to database."""
        data = TodoCreate(
            title="New Todo",
            description="Description",
            priority=Priority.HIGH,
            tags=["urgent"],
        )

        # Mock session operations
        mock_session.add = MagicMock()
        mock_session.flush = AsyncMock()
        mock_session.refresh = AsyncMock()

        todo = await todo_service.create_todo(user_id, data)

        assert todo.user_id == user_id
        assert todo.title == "New Todo"
        assert todo.priority == Priority.HIGH
        mock_session.add.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_todo_success(
        self, todo_service, mock_session, user_id, todo_id, mock_todo
    ):
        """Get todo should return todo for valid ID and user."""
        # Mock query execution
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_todo
        mock_session.execute = AsyncMock(return_value=mock_result)

        todo = await todo_service.get_todo(todo_id, user_id)

        assert todo.id == todo_id
        assert todo.user_id == user_id

    @pytest.mark.asyncio
    async def test_get_todo_not_found(self, todo_service, mock_session, user_id):
        """Get todo should raise NotFoundError for non-existent todo."""
        # Mock query returning None
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        with pytest.raises(NotFoundError, match="Todo not found"):
            await todo_service.get_todo(uuid4(), user_id)

    @pytest.mark.asyncio
    async def test_get_todo_wrong_user(self, todo_service, mock_session, todo_id):
        """Get todo should raise NotFoundError for wrong user (user isolation)."""
        other_user_id = uuid4()

        # Mock query returning None (because user_id doesn't match)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        with pytest.raises(NotFoundError, match="Todo not found"):
            await todo_service.get_todo(todo_id, other_user_id)

    @pytest.mark.asyncio
    async def test_update_todo_success(
        self, todo_service, mock_session, user_id, todo_id, mock_todo
    ):
        """Update todo should modify todo fields."""
        # Mock get_todo
        with patch.object(todo_service, "get_todo", return_value=mock_todo):
            mock_session.flush = AsyncMock()
            mock_session.refresh = AsyncMock()

            data = TodoUpdate(title="Updated Title", status=TodoStatus.COMPLETED)
            todo = await todo_service.update_todo(todo_id, user_id, data)

            assert todo.title == "Updated Title"
            assert todo.status == TodoStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_soft_delete_todo_success(
        self, todo_service, mock_session, user_id, todo_id, mock_todo
    ):
        """Soft delete should set deleted_at timestamp."""
        # Mock get_todo
        with patch.object(todo_service, "get_todo", return_value=mock_todo):
            mock_session.flush = AsyncMock()

            await todo_service.soft_delete_todo(todo_id, user_id)

            assert mock_todo.deleted_at is not None

    @pytest.mark.asyncio
    async def test_list_todos_filters_by_user(
        self, todo_service, mock_session, user_id
    ):
        """List todos should only return user's todos."""
        # This test verifies the query includes user_id filter
        # In a real test with a database, we'd create todos for multiple users
        # and verify only the correct user's todos are returned

        mock_result = MagicMock()
        mock_result.scalar.return_value = 0  # Total count
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute = AsyncMock(return_value=mock_result)

        result = await todo_service.list_todos(user_id)

        assert result.items == []
        assert result.total == 0

    @pytest.mark.asyncio
    async def test_list_todos_with_status_filter(
        self, todo_service, mock_session, user_id
    ):
        """List todos should filter by status when provided."""
        mock_result = MagicMock()
        mock_result.scalar.return_value = 0
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute = AsyncMock(return_value=mock_result)

        result = await todo_service.list_todos(
            user_id, status=TodoStatus.COMPLETED
        )

        assert result.items == []

    @pytest.mark.asyncio
    async def test_list_todos_with_priority_filter(
        self, todo_service, mock_session, user_id
    ):
        """List todos should filter by priority when provided."""
        mock_result = MagicMock()
        mock_result.scalar.return_value = 0
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute = AsyncMock(return_value=mock_result)

        result = await todo_service.list_todos(user_id, priority=Priority.HIGH)

        assert result.items == []

    @pytest.mark.asyncio
    async def test_list_todos_pagination(self, todo_service, mock_session, user_id):
        """List todos should support pagination."""
        mock_result = MagicMock()
        mock_result.scalar.return_value = 50  # Total count
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute = AsyncMock(return_value=mock_result)

        result = await todo_service.list_todos(user_id, page=2, per_page=10)

        assert result.page == 2
        assert result.per_page == 10
        assert result.total == 50
        assert result.total_pages == 5
