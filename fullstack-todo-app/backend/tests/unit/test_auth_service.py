"""Unit tests for auth service."""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from app.models.user import User
from app.security.password import hash_password
from app.services.auth_service import AuthService
from app.utils.exceptions import AuthenticationError, ConflictError


class TestAuthService:
    """Tests for AuthService."""

    @pytest.fixture
    def mock_session(self):
        """Create mock database session."""
        return AsyncMock()

    @pytest.fixture
    def auth_service(self, mock_session):
        """Create auth service with mock session."""
        return AuthService(mock_session)

    @pytest.fixture
    def mock_user(self):
        """Create mock user."""
        return User(
            id=uuid4(),
            email="test@example.com",
            username="testuser",
            password_hash=hash_password("TestPassword123"),
        )

    @pytest.mark.asyncio
    async def test_register_user_success(self, auth_service, mock_session):
        """Register should create user and return tokens."""
        # Mock user_service methods
        with patch.object(
            auth_service.user_service, "get_by_email", return_value=None
        ), patch.object(
            auth_service.user_service, "get_by_username", return_value=None
        ), patch.object(
            auth_service.user_service, "create", new_callable=AsyncMock
        ) as mock_create:
            mock_user = User(
                id=uuid4(),
                email="new@example.com",
                username="newuser",
                password_hash="hashed",
            )
            mock_create.return_value = mock_user

            user, token_data, refresh_token = await auth_service.register_user(
                email="new@example.com",
                username="newuser",
                password="TestPassword123",
            )

            assert user.email == "new@example.com"
            assert token_data.access_token is not None
            assert refresh_token is not None

    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, auth_service, mock_user):
        """Authenticate should return tokens for valid credentials."""
        with patch.object(
            auth_service.user_service, "get_by_email", return_value=mock_user
        ):
            user, token_data, refresh_token = await auth_service.authenticate_user(
                email="test@example.com",
                password="TestPassword123",
            )

            assert user.id == mock_user.id
            assert token_data.access_token is not None
            assert refresh_token is not None

    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self, auth_service, mock_user):
        """Authenticate should raise error for wrong password."""
        with patch.object(
            auth_service.user_service, "get_by_email", return_value=mock_user
        ):
            with pytest.raises(AuthenticationError, match="Invalid credentials"):
                await auth_service.authenticate_user(
                    email="test@example.com",
                    password="WrongPassword",
                )

    @pytest.mark.asyncio
    async def test_authenticate_user_not_found(self, auth_service):
        """Authenticate should raise error for non-existent user."""
        with patch.object(
            auth_service.user_service, "get_by_email", return_value=None
        ):
            with pytest.raises(AuthenticationError, match="Invalid credentials"):
                await auth_service.authenticate_user(
                    email="nonexistent@example.com",
                    password="TestPassword123",
                )

    @pytest.mark.asyncio
    async def test_refresh_tokens_success(self, auth_service, mock_user):
        """Refresh should return new token pair."""
        with patch.object(
            auth_service.user_service, "get_by_id", return_value=mock_user
        ):
            token_data, refresh_token = await auth_service.refresh_tokens(
                user_id=mock_user.id
            )

            assert token_data.access_token is not None
            assert refresh_token is not None

    @pytest.mark.asyncio
    async def test_refresh_tokens_user_not_found(self, auth_service):
        """Refresh should raise error for non-existent user."""
        with patch.object(
            auth_service.user_service, "get_by_id", return_value=None
        ):
            with pytest.raises(AuthenticationError, match="User not found"):
                await auth_service.refresh_tokens(user_id=uuid4())

    def test_create_tokens(self, auth_service):
        """Create tokens should return token pair."""
        user_id = uuid4()
        token_data, refresh_token = auth_service.create_tokens(user_id)

        assert token_data.access_token is not None
        assert token_data.token_type == "bearer"
        assert refresh_token is not None
