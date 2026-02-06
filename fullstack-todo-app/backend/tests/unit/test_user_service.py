"""Unit tests for user service."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas import UserUpdate
from app.models.user import User
from app.services.user_service import UserService
from app.utils.exceptions import ConflictError, NotFoundError


class TestUserService:
    """Tests for UserService."""

    @pytest.fixture
    def mock_session(self):
        """Create mock database session."""
        session = AsyncMock(spec=AsyncSession)
        return session

    @pytest.fixture
    def user_service(self, mock_session):
        """Create user service with mock session."""
        return UserService(mock_session)

    @pytest.fixture
    def user_id(self):
        """Create test user ID."""
        return uuid4()

    @pytest.fixture
    def mock_user(self, user_id):
        """Create mock user."""
        return User(
            id=user_id,
            email="test@example.com",
            username="testuser",
            password_hash="hashed_password",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, user_service, mock_session, user_id, mock_user
    ):
        """Get user by ID should return user for valid ID."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_session.execute = AsyncMock(return_value=mock_result)

        user = await user_service.get_by_id(user_id)

        assert user is not None
        assert user.id == user_id
        assert user.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, user_service, mock_session):
        """Get user by ID should return None for non-existent user."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        user = await user_service.get_by_id(uuid4())

        assert user is None

    @pytest.mark.asyncio
    async def test_get_by_email_success(
        self, user_service, mock_session, mock_user
    ):
        """Get user by email should return user for valid email."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_session.execute = AsyncMock(return_value=mock_result)

        user = await user_service.get_by_email("test@example.com")

        assert user is not None
        assert user.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_by_email_not_found(self, user_service, mock_session):
        """Get user by email should return None for non-existent email."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        user = await user_service.get_by_email("nonexistent@example.com")

        assert user is None

    @pytest.mark.asyncio
    async def test_get_by_username_success(
        self, user_service, mock_session, mock_user
    ):
        """Get user by username should return user for valid username."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_session.execute = AsyncMock(return_value=mock_result)

        user = await user_service.get_by_username("testuser")

        assert user is not None
        assert user.username == "testuser"

    @pytest.mark.asyncio
    async def test_get_by_username_not_found(self, user_service, mock_session):
        """Get user by username should return None for non-existent username."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        user = await user_service.get_by_username("nonexistent")

        assert user is None

    @pytest.mark.asyncio
    async def test_update_user_username_success(
        self, user_service, mock_session, user_id, mock_user
    ):
        """Update user should change username when new username is available."""
        # Mock get_by_id to return the user
        mock_result_user = MagicMock()
        mock_result_user.scalar_one_or_none.return_value = mock_user

        # Mock get_by_username to return None (username available)
        mock_result_check = MagicMock()
        mock_result_check.scalar_one_or_none.return_value = None

        mock_session.execute = AsyncMock(
            side_effect=[mock_result_user, mock_result_check]
        )
        mock_session.flush = AsyncMock()
        mock_session.refresh = AsyncMock()

        data = UserUpdate(username="newusername")
        user = await user_service.update_user(user_id, data)

        assert user.username == "newusername"

    @pytest.mark.asyncio
    async def test_update_user_username_conflict(
        self, user_service, mock_session, user_id, mock_user
    ):
        """Update user should raise ConflictError when username is taken."""
        other_user = User(
            id=uuid4(),
            email="other@example.com",
            username="newusername",
            password_hash="hashed",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        # Mock get_by_id to return the user
        mock_result_user = MagicMock()
        mock_result_user.scalar_one_or_none.return_value = mock_user

        # Mock get_by_username to return existing user (username taken)
        mock_result_check = MagicMock()
        mock_result_check.scalar_one_or_none.return_value = other_user

        mock_session.execute = AsyncMock(
            side_effect=[mock_result_user, mock_result_check]
        )

        data = UserUpdate(username="newusername")
        with pytest.raises(ConflictError, match="Username already taken"):
            await user_service.update_user(user_id, data)

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, user_service, mock_session):
        """Update user should raise NotFoundError for non-existent user."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        data = UserUpdate(username="newusername")
        with pytest.raises(NotFoundError, match="User not found"):
            await user_service.update_user(uuid4(), data)

    @pytest.mark.asyncio
    async def test_update_user_same_username_no_check(
        self, user_service, mock_session, user_id, mock_user
    ):
        """Update user with same username should not trigger conflict check."""
        # Mock get_by_id to return the user
        mock_result_user = MagicMock()
        mock_result_user.scalar_one_or_none.return_value = mock_user

        mock_session.execute = AsyncMock(return_value=mock_result_user)
        mock_session.flush = AsyncMock()
        mock_session.refresh = AsyncMock()

        # Update with same username
        data = UserUpdate(username="testuser")
        user = await user_service.update_user(user_id, data)

        # Should succeed without conflict check
        assert user.username == "testuser"
