"""Integration tests for users API endpoints."""

import pytest
from httpx import AsyncClient


class TestUsersAPI:
    """Tests for /users endpoints."""

    @pytest.fixture
    async def auth_headers(self, client: AsyncClient, test_user):
        """Get authentication headers for test user."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user["email"],
                "password": test_user["password"],
            },
        )
        data = response.json()
        return {"Authorization": f"Bearer {data['data']['access_token']}"}

    @pytest.mark.asyncio
    async def test_get_profile_success(
        self, client: AsyncClient, auth_headers, test_user
    ):
        """GET /users/me should return current user's profile."""
        response = await client.get("/api/v1/users/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == test_user["email"]
        assert data["data"]["username"] == test_user["username"]
        assert "password_hash" not in data["data"]

    @pytest.mark.asyncio
    async def test_get_profile_unauthorized(self, client: AsyncClient):
        """GET /users/me without auth should return 401."""
        response = await client.get("/api/v1/users/me")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_profile_invalid_token(self, client: AsyncClient):
        """GET /users/me with invalid token should return 401."""
        response = await client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_update_profile_username_success(
        self, client: AsyncClient, auth_headers
    ):
        """PATCH /users/me should update username."""
        response = await client.patch(
            "/api/v1/users/me",
            headers=auth_headers,
            json={"username": "newusername"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["username"] == "newusername"

    @pytest.mark.asyncio
    async def test_update_profile_username_conflict(
        self, client: AsyncClient, auth_headers, test_user_2
    ):
        """PATCH /users/me with existing username should return 409."""
        response = await client.patch(
            "/api/v1/users/me",
            headers=auth_headers,
            json={"username": test_user_2["username"]},
        )

        assert response.status_code == 409
        data = response.json()
        assert data["success"] is False
        assert "already taken" in data["error"].lower()

    @pytest.mark.asyncio
    async def test_update_profile_username_validation(
        self, client: AsyncClient, auth_headers
    ):
        """PATCH /users/me with invalid username should return 422."""
        # Username too short
        response = await client.patch(
            "/api/v1/users/me",
            headers=auth_headers,
            json={"username": "ab"},  # Less than 3 characters
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_update_profile_unauthorized(self, client: AsyncClient):
        """PATCH /users/me without auth should return 401."""
        response = await client.patch(
            "/api/v1/users/me",
            json={"username": "newusername"},
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_update_profile_same_username(
        self, client: AsyncClient, auth_headers, test_user
    ):
        """PATCH /users/me with same username should succeed."""
        response = await client.patch(
            "/api/v1/users/me",
            headers=auth_headers,
            json={"username": test_user["username"]},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["username"] == test_user["username"]

    @pytest.mark.asyncio
    async def test_update_profile_empty_body(
        self, client: AsyncClient, auth_headers
    ):
        """PATCH /users/me with empty body should return 422."""
        response = await client.patch(
            "/api/v1/users/me",
            headers=auth_headers,
            json={},
        )

        # Empty update should return validation error
        assert response.status_code == 422
