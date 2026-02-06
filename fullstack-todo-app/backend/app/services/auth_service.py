"""Authentication service for user registration and login."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas import TokenData
from app.models.user import User
from app.security.jwt import create_access_token, create_refresh_token
from app.security.password import hash_password, verify_password
from app.services.user_service import UserService
from app.utils.exceptions import AuthenticationError, ConflictError


class AuthService:
    """Service for authentication operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session
        self.user_service = UserService(session)

    async def register_user(
        self,
        email: str,
        username: str,
        password: str,
    ) -> tuple[User, TokenData, str]:
        """
        Register a new user and return tokens.

        Args:
            email: User's email address
            username: User's username
            password: Plain text password

        Returns:
            Tuple of (user, access_token_data, refresh_token)

        Raises:
            ConflictError: If email or username already exists
        """
        # Hash password with bcrypt (12+ rounds per constitution)
        password_hash = hash_password(password)

        # Create user
        user = await self.user_service.create(
            email=email,
            username=username,
            password_hash=password_hash,
        )

        # Generate tokens
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return user, TokenData(access_token=access_token), refresh_token

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> tuple[User, TokenData, str]:
        """
        Authenticate user with email and password.

        Args:
            email: User's email address
            password: Plain text password

        Returns:
            Tuple of (user, access_token_data, refresh_token)

        Raises:
            AuthenticationError: If credentials are invalid
        """
        user = await self.user_service.get_by_email(email)

        # Generic error to prevent user enumeration
        if not user:
            raise AuthenticationError("Invalid credentials")

        if not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid credentials")

        # Generate tokens
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return user, TokenData(access_token=access_token), refresh_token

    async def refresh_tokens(self, user_id: UUID) -> tuple[TokenData, str]:
        """
        Generate new token pair for user (token rotation).

        Args:
            user_id: User's unique identifier

        Returns:
            Tuple of (access_token_data, new_refresh_token)

        Raises:
            AuthenticationError: If user not found
        """
        user = await self.user_service.get_by_id(user_id)

        if not user or user.is_deleted:
            raise AuthenticationError("User not found")

        # Generate new tokens (rotation - old refresh token is now invalid)
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return TokenData(access_token=access_token), refresh_token

    def create_tokens(self, user_id: UUID) -> tuple[TokenData, str]:
        """
        Create token pair for a user.

        Args:
            user_id: User's unique identifier

        Returns:
            Tuple of (access_token_data, refresh_token)
        """
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)

        return TokenData(access_token=access_token), refresh_token
