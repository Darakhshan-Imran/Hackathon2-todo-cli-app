"""Integration tests for todos API endpoints."""

from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import Priority, TodoStatus
from app.models.todo import Todo
from app.models.user import User


@pytest.fixture
async def test_todo(test_session: AsyncSession, test_user: User) -> Todo:
    """Create a test todo."""
    todo = Todo(
        id=uuid4(),
        user_id=test_user.id,
        title="Test Todo",
        description="Test description",
        status=TodoStatus.PENDING,
        priority=Priority.MEDIUM,
        tags=["test"],
    )
    test_session.add(todo)
    await test_session.commit()
    await test_session.refresh(todo)
    return todo


class TestListTodos:
    """Tests for GET /api/v1/todos."""

    @pytest.mark.asyncio
    async def test_list_todos_success(
        self, client: AsyncClient, auth_headers: dict, test_todo: Todo
    ):
        """List todos should return user's todos."""
        response = await client.get("/api/v1/todos", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "items" in data["data"]
        assert len(data["data"]["items"]) >= 1
        assert data["data"]["items"][0]["title"] == "Test Todo"

    @pytest.mark.asyncio
    async def test_list_todos_pagination(
        self, client: AsyncClient, auth_headers: dict
    ):
        """List todos should support pagination."""
        response = await client.get(
            "/api/v1/todos?page=1&per_page=5",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["page"] == 1
        assert data["data"]["per_page"] == 5

    @pytest.mark.asyncio
    async def test_list_todos_filter_status(
        self, client: AsyncClient, auth_headers: dict, test_todo: Todo
    ):
        """List todos should filter by status."""
        response = await client.get(
            "/api/v1/todos?status=pending",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        for item in data["data"]["items"]:
            assert item["status"] == "pending"

    @pytest.mark.asyncio
    async def test_list_todos_unauthorized(self, client: AsyncClient):
        """List todos should require authentication."""
        response = await client.get("/api/v1/todos")

        assert response.status_code == 401


class TestCreateTodo:
    """Tests for POST /api/v1/todos."""

    @pytest.mark.asyncio
    async def test_create_todo_success(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Create todo should return new todo."""
        response = await client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={
                "title": "New Todo",
                "description": "New description",
                "priority": "high",
                "tags": ["important"],
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "New Todo"
        assert data["data"]["status"] == "pending"  # Default
        assert data["data"]["priority"] == "high"

    @pytest.mark.asyncio
    async def test_create_todo_minimal(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Create todo should work with only title."""
        response = await client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"title": "Minimal Todo"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["data"]["title"] == "Minimal Todo"
        assert data["data"]["status"] == "pending"
        assert data["data"]["priority"] == "medium"

    @pytest.mark.asyncio
    async def test_create_todo_empty_title(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Create todo should fail without title."""
        response = await client.post(
            "/api/v1/todos",
            headers=auth_headers,
            json={"description": "No title"},
        )

        assert response.status_code == 422


class TestGetTodo:
    """Tests for GET /api/v1/todos/{id}."""

    @pytest.mark.asyncio
    async def test_get_todo_success(
        self, client: AsyncClient, auth_headers: dict, test_todo: Todo
    ):
        """Get todo should return todo details."""
        response = await client.get(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == str(test_todo.id)
        assert data["data"]["title"] == "Test Todo"

    @pytest.mark.asyncio
    async def test_get_todo_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Get todo should return 404 for non-existent todo."""
        response = await client.get(
            f"/api/v1/todos/{uuid4()}",
            headers=auth_headers,
        )

        assert response.status_code == 404


class TestUpdateTodo:
    """Tests for PATCH /api/v1/todos/{id}."""

    @pytest.mark.asyncio
    async def test_update_todo_success(
        self, client: AsyncClient, auth_headers: dict, test_todo: Todo
    ):
        """Update todo should modify todo fields."""
        response = await client.patch(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers,
            json={
                "title": "Updated Title",
                "status": "completed",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "Updated Title"
        assert data["data"]["status"] == "completed"

    @pytest.mark.asyncio
    async def test_update_todo_partial(
        self, client: AsyncClient, auth_headers: dict, test_todo: Todo
    ):
        """Update should only modify provided fields."""
        original_title = test_todo.title
        response = await client.patch(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers,
            json={"priority": "high"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == original_title  # Unchanged
        assert data["data"]["priority"] == "high"  # Changed


class TestDeleteTodo:
    """Tests for DELETE /api/v1/todos/{id}."""

    @pytest.mark.asyncio
    async def test_delete_todo_success(
        self, client: AsyncClient, auth_headers: dict, test_todo: Todo
    ):
        """Delete todo should soft delete."""
        response = await client.delete(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        # Verify it's not visible anymore
        get_response = await client.get(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers,
        )
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_todo_not_found(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Delete should return 404 for non-existent todo."""
        response = await client.delete(
            f"/api/v1/todos/{uuid4()}",
            headers=auth_headers,
        )

        assert response.status_code == 404
