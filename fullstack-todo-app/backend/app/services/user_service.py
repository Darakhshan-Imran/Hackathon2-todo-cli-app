"""User service for user CRUD operations."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.user import User
from app.utils.exceptions import ConflictError, NotFoundError


class UserService:
    """Service for user-related operations."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        """
        Get user by ID.

        Args:
            user_id: User's unique identifier

        Returns:
            User if found and not deleted, None otherwise
        """
        query = select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """
        Get user by email address.

        Args:
            email: User's email address

        Returns:
            User if found and not deleted, None otherwise
        """
        query = select(User).where(
            User.email == email.lower(),
            User.deleted_at.is_(None),
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        """
        Get user by username.

        Args:
            username: User's username

        Returns:
            User if found and not deleted, None otherwise
        """
        query = select(User).where(
            User.username == username,
            User.deleted_at.is_(None),
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(
        self,
        email: str,
        username: str,
        password_hash: str,
    ) -> User:
        """
        Create a new user.

        Args:
            email: User's email address
            username: User's username
            password_hash: Bcrypt hashed password

        Returns:
            Created user

        Raises:
            ConflictError: If email or username already exists
        """
        # Check for existing email
        existing_email = await self.get_by_email(email)
        if existing_email:
            raise ConflictError("Email already registered")

        # Check for existing username
        existing_username = await self.get_by_username(username)
        if existing_username:
            raise ConflictError("Username already taken")

        user = User(
            email=email.lower(),
            username=username,
            password_hash=password_hash,
        )

        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)

        return user

    async def update_username(self, user_id: UUID, new_username: str) -> User:
        """
        Update user's username.

        Args:
            user_id: User's unique identifier
            new_username: New username

        Returns:
            Updated user

        Raises:
            NotFoundError: If user not found
            ConflictError: If username already taken by another user
        """
        user = await self.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        # Check if new username is taken by someone else
        existing = await self.get_by_username(new_username)
        if existing and existing.id != user_id:
            raise ConflictError("Username already taken")

        user.username = new_username
        await self.session.flush()
        await self.session.refresh(user)

        return user
