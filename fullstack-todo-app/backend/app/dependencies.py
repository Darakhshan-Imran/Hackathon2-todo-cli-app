"""FastAPI dependencies for dependency injection."""

from collections.abc import AsyncGenerator
from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import get_session_factory
from app.models.user import User
from app.security.jwt import TokenError, get_user_id_from_token, verify_token
from app.services.user_service import UserService
from app.utils.exceptions import AuthenticationError

_bearer_scheme = HTTPBearer()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get async database session.

    Yields:
        AsyncSession: Database session that auto-closes after request
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer_scheme)],
    session: AsyncSession = Depends(get_db_session),
) -> User:
    """
    Dependency to get the current authenticated user from JWT.

    Args:
        credentials: Bearer token extracted by HTTPBearer
        session: Database session

    Returns:
        User: Authenticated user

    Raises:
        AuthenticationError: If token is missing, invalid, or user not found
    """
    try:
        user_id = get_user_id_from_token(credentials.credentials, token_type="access")
    except TokenError as e:
        raise AuthenticationError(str(e)) from e

    # Get user from database
    user_service = UserService(session)
    user = await user_service.get_by_id(user_id)

    if user is None or user.is_deleted:
        raise AuthenticationError("User not found")

    return user


async def get_refresh_token_user_id(
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> UUID:
    """
    Dependency to extract user ID from refresh token cookie.

    Args:
        refresh_token: Refresh token from HttpOnly cookie

    Returns:
        UUID: User ID from token

    Raises:
        AuthenticationError: If token is missing or invalid
    """
    if not refresh_token:
        raise AuthenticationError("Refresh token required")

    try:
        return get_user_id_from_token(refresh_token, token_type="refresh")
    except TokenError as e:
        raise AuthenticationError(str(e)) from e


# Type aliases for cleaner dependency injection
DbSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
RefreshTokenUserId = Annotated[UUID, Depends(get_refresh_token_user_id)]
