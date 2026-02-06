"""Integration tests for user data isolation."""

from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import Priority, TodoStatus
from app.models.todo import Todo
from app.models.user import User


@pytest.fixture
async def user1_todo(test_session: AsyncSession, test_user: User) -> Todo:
    """Create a todo for user 1."""
    todo = Todo(
        id=uuid4(),
        user_id=test_user.id,
        title="User 1 Todo",
        description="Private to user 1",
        status=TodoStatus.PENDING,
        priority=Priority.HIGH,
    )
    test_session.add(todo)
    await test_session.commit()
    await test_session.refresh(todo)
    return todo


@pytest.fixture
async def user2_todo(test_session: AsyncSession, test_user_2: User) -> Todo:
    """Create a todo for user 2."""
    todo = Todo(
        id=uuid4(),
        user_id=test_user_2.id,
        title="User 2 Todo",
        description="Private to user 2",
        status=TodoStatus.PENDING,
        priority=Priority.LOW,
    )
    test_session.add(todo)
    await test_session.commit()
    await test_session.refresh(todo)
    return todo


class TestUserIsolation:
    """Tests verifying users cannot access other users' data."""

    @pytest.mark.asyncio
    async def test_user_cannot_get_other_users_todo(
        self,
        client: AsyncClient,
        auth_headers: dict,  # User 1's token
        user2_todo: Todo,  # User 2's todo
    ):
        """User should get 404 when accessing another user's todo."""
        response = await client.get(
            f"/api/v1/todos/{user2_todo.id}",
            headers=auth_headers,
        )

        # Should return 404, not 403 (to prevent enumeration)
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["error"].lower()

    @pytest.mark.asyncio
    async def test_user_cannot_update_other_users_todo(
        self,
        client: AsyncClient,
        auth_headers: dict,  # User 1's token
        user2_todo: Todo,  # User 2's todo
    ):
        """User should get 404 when updating another user's todo."""
        response = await client.patch(
            f"/api/v1/todos/{user2_todo.id}",
            headers=auth_headers,
            json={"title": "Hacked!"},
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_user_cannot_delete_other_users_todo(
        self,
        client: AsyncClient,
        auth_headers: dict,  # User 1's token
        user2_todo: Todo,  # User 2's todo
    ):
        """User should get 404 when deleting another user's todo."""
        response = await client.delete(
            f"/api/v1/todos/{user2_todo.id}",
            headers=auth_headers,
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_only_shows_own_todos(
        self,
        client: AsyncClient,
        auth_headers: dict,  # User 1's token
        auth_headers_user2: dict,  # User 2's token
        user1_todo: Todo,
        user2_todo: Todo,
    ):
        """List should only show user's own todos."""
        # User 1 list
        response1 = await client.get(
            "/api/v1/todos",
            headers=auth_headers,
        )
        data1 = response1.json()
        todo_ids_1 = [item["id"] for item in data1["data"]["items"]]

        # User 2 list
        response2 = await client.get(
            "/api/v1/todos",
            headers=auth_headers_user2,
        )
        data2 = response2.json()
        todo_ids_2 = [item["id"] for item in data2["data"]["items"]]

        # Verify isolation
        assert str(user1_todo.id) in todo_ids_1
        assert str(user2_todo.id) not in todo_ids_1

        assert str(user2_todo.id) in todo_ids_2
        assert str(user1_todo.id) not in todo_ids_2

    @pytest.mark.asyncio
    async def test_user2_can_access_own_todo(
        self,
        client: AsyncClient,
        auth_headers_user2: dict,  # User 2's token
        user2_todo: Todo,  # User 2's todo
    ):
        """User should be able to access their own todo."""
        response = await client.get(
            f"/api/v1/todos/{user2_todo.id}",
            headers=auth_headers_user2,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "User 2 Todo"

    @pytest.mark.asyncio
    async def test_user2_can_update_own_todo(
        self,
        client: AsyncClient,
        auth_headers_user2: dict,
        user2_todo: Todo,
    ):
        """User should be able to update their own todo."""
        response = await client.patch(
            f"/api/v1/todos/{user2_todo.id}",
            headers=auth_headers_user2,
            json={"title": "Updated by owner"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "Updated by owner"

    @pytest.mark.asyncio
    async def test_user2_can_delete_own_todo(
        self,
        client: AsyncClient,
        auth_headers_user2: dict,
        user2_todo: Todo,
    ):
        """User should be able to delete their own todo."""
        response = await client.delete(
            f"/api/v1/todos/{user2_todo.id}",
            headers=auth_headers_user2,
        )

        assert response.status_code == 200
