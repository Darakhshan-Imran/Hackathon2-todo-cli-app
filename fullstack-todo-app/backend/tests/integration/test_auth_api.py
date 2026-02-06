"""Integration tests for auth API endpoints."""

import pytest
from httpx import AsyncClient

from app.models.user import User


class TestAuthSignup:
    """Tests for POST /api/v1/auth/signup."""

    @pytest.mark.asyncio
    async def test_signup_success(self, client: AsyncClient):
        """Signup should create user and return tokens."""
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "TestPassword123",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"
        assert "timestamp" in data

        # Check refresh token cookie
        assert "refresh_token" in response.cookies

    @pytest.mark.asyncio
    async def test_signup_duplicate_email(self, client: AsyncClient, test_user: User):
        """Signup should fail for duplicate email."""
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": test_user.email,
                "username": "differentuser",
                "password": "TestPassword123",
            },
        )

        assert response.status_code == 409
        data = response.json()
        assert data["success"] is False
        assert "already registered" in data["error"].lower()

    @pytest.mark.asyncio
    async def test_signup_duplicate_username(
        self, client: AsyncClient, test_user: User
    ):
        """Signup should fail for duplicate username."""
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "different@example.com",
                "username": test_user.username,
                "password": "TestPassword123",
            },
        )

        assert response.status_code == 409
        data = response.json()
        assert data["success"] is False
        assert "already taken" in data["error"].lower()

    @pytest.mark.asyncio
    async def test_signup_invalid_email(self, client: AsyncClient):
        """Signup should fail for invalid email format."""
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "not-an-email",
                "username": "newuser",
                "password": "TestPassword123",
            },
        )

        assert response.status_code == 422  # Pydantic validation error

    @pytest.mark.asyncio
    async def test_signup_short_password(self, client: AsyncClient):
        """Signup should fail for password < 8 characters."""
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "short",
            },
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_signup_invalid_username(self, client: AsyncClient):
        """Signup should fail for invalid username format."""
        response = await client.post(
            "/api/v1/auth/signup",
            json={
                "email": "newuser@example.com",
                "username": "invalid username!",  # Contains space and special char
                "password": "TestPassword123",
            },
        )

        assert response.status_code == 422


class TestAuthLogin:
    """Tests for POST /api/v1/auth/login."""

    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user: User):
        """Login should return tokens for valid credentials."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "TestPassword123",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert "refresh_token" in response.cookies

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient, test_user: User):
        """Login should fail for wrong password."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "WrongPassword",
            },
        )

        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert "invalid credentials" in data["error"].lower()

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Login should fail for non-existent user."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "TestPassword123",
            },
        )

        assert response.status_code == 401
        data = response.json()
        # Should show same error to prevent user enumeration
        assert "invalid credentials" in data["error"].lower()


class TestAuthRefresh:
    """Tests for POST /api/v1/auth/refresh."""

    @pytest.mark.asyncio
    async def test_refresh_success(self, client: AsyncClient, test_user: User):
        """Refresh should return new tokens."""
        # First login to get refresh token
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "TestPassword123",
            },
        )
        refresh_token = login_response.cookies.get("refresh_token")

        # Now refresh
        response = await client.post(
            "/api/v1/auth/refresh",
            cookies={"refresh_token": refresh_token},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]

    @pytest.mark.asyncio
    async def test_refresh_no_cookie(self, client: AsyncClient):
        """Refresh should fail without refresh token cookie."""
        response = await client.post("/api/v1/auth/refresh")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_refresh_invalid_token(self, client: AsyncClient):
        """Refresh should fail with invalid token."""
        response = await client.post(
            "/api/v1/auth/refresh",
            cookies={"refresh_token": "invalid-token"},
        )

        assert response.status_code == 401


class TestAuthLogout:
    """Tests for POST /api/v1/auth/logout."""

    @pytest.mark.asyncio
    async def test_logout_success(
        self, client: AsyncClient, test_user: User, auth_headers: dict
    ):
        """Logout should clear refresh token cookie."""
        response = await client.post(
            "/api/v1/auth/logout",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    @pytest.mark.asyncio
    async def test_logout_unauthorized(self, client: AsyncClient):
        """Logout should fail without auth token."""
        response = await client.post("/api/v1/auth/logout")

        assert response.status_code == 401
