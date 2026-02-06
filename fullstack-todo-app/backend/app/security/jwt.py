"""JWT token creation and verification."""

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

from jose import JWTError, jwt

from app.config import get_settings


class TokenError(Exception):
    """Raised when token validation fails."""

    pass


def create_access_token(user_id: UUID) -> str:
    """
    Create a JWT access token.

    Args:
        user_id: User's unique identifier

    Returns:
        Encoded JWT access token (valid for 15 minutes)
    """
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(user_id: UUID) -> str:
    """
    Create a JWT refresh token.

    Args:
        user_id: User's unique identifier

    Returns:
        Encoded JWT refresh token (valid for 7 days)
    """
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "jti": str(uuid4()),  # Unique token ID for rotation tracking
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def verify_token(token: str, token_type: str = "access") -> dict[str, Any]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string
        token_type: Expected token type ("access" or "refresh")

    Returns:
        Decoded token payload

    Raises:
        TokenError: If token is invalid, expired, or wrong type
    """
    settings = get_settings()

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError as e:
        raise TokenError(f"Invalid token: {e}") from e

    # Verify token type
    if payload.get("type") != token_type:
        raise TokenError(f"Invalid token type. Expected {token_type}")

    # Verify subject exists
    if not payload.get("sub"):
        raise TokenError("Token missing subject claim")

    return payload


def get_user_id_from_token(token: str, token_type: str = "access") -> UUID:
    """
    Extract user ID from a verified token.

    Args:
        token: JWT token string
        token_type: Expected token type

    Returns:
        User UUID

    Raises:
        TokenError: If token is invalid or user_id cannot be extracted
    """
    payload = verify_token(token, token_type)
    try:
        return UUID(payload["sub"])
    except (KeyError, ValueError) as e:
        raise TokenError("Invalid user ID in token") from e
