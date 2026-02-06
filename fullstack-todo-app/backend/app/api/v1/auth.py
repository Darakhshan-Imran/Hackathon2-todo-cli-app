"""Authentication endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.dependencies import CurrentUser, DbSession, RefreshTokenUserId
from app.models.schemas import APIResponse, LoginRequest, SignupRequest, TokenData
from app.services.auth_service import AuthService
from app.utils.logger import log_security_event

router = APIRouter()


def _get_client_ip(request: Request) -> str:
    """Extract client IP address from request."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    """Set HttpOnly refresh token cookie."""
    settings = get_settings()
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.is_production,
        samesite="strict",
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        path="/api/v1/auth",
    )


def _clear_refresh_cookie(response: Response) -> None:
    """Clear refresh token cookie."""
    response.delete_cookie(
        key="refresh_token",
        path="/api/v1/auth",
    )


@router.post("/signup", status_code=201)
async def signup(
    data: SignupRequest,
    request: Request,
    response: Response,
    session: DbSession,
) -> APIResponse[TokenData]:
    """
    Create new user account.

    Returns access token in response body and refresh token in HttpOnly cookie.
    """
    auth_service = AuthService(session)
    user, token_data, refresh_token = await auth_service.register_user(
        email=data.email,
        username=data.username,
        password=data.password,
    )

    # Set refresh token cookie
    _set_refresh_cookie(response, refresh_token)

    # Log security event
    log_security_event(
        event_type="signup",
        user_id=str(user.id),
        ip_address=_get_client_ip(request),
        success=True,
    )

    return APIResponse(
        success=True,
        data=token_data,
        timestamp=datetime.now(timezone.utc),
    )


@router.post("/login")
async def login(
    data: LoginRequest,
    request: Request,
    response: Response,
    session: DbSession,
) -> APIResponse[TokenData]:
    """
    Authenticate user and get tokens.

    Returns access token in response body and refresh token in HttpOnly cookie.
    """
    auth_service = AuthService(session)

    try:
        user, token_data, refresh_token = await auth_service.authenticate_user(
            email=data.email,
            password=data.password,
        )
    except Exception:
        # Log failed authentication
        log_security_event(
            event_type="login",
            ip_address=_get_client_ip(request),
            success=False,
            details="Invalid credentials",
        )
        raise

    # Set refresh token cookie
    _set_refresh_cookie(response, refresh_token)

    # Log successful login
    log_security_event(
        event_type="login",
        user_id=str(user.id),
        ip_address=_get_client_ip(request),
        success=True,
    )

    return APIResponse(
        success=True,
        data=token_data,
        timestamp=datetime.now(timezone.utc),
    )


@router.post("/refresh")
async def refresh_token(
    response: Response,
    user_id: RefreshTokenUserId,
    session: DbSession,
) -> APIResponse[TokenData]:
    """
    Get new access token using refresh token cookie.

    Implements token rotation - issues new refresh token and invalidates old one.
    """
    auth_service = AuthService(session)
    token_data, new_refresh_token = await auth_service.refresh_tokens(user_id)

    # Set new refresh token cookie (rotation)
    _set_refresh_cookie(response, new_refresh_token)

    return APIResponse(
        success=True,
        data=token_data,
        timestamp=datetime.now(timezone.utc),
    )


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    current_user: CurrentUser,
) -> APIResponse[None]:
    """
    Logout user by clearing refresh token cookie.

    Note: This doesn't invalidate the access token - it will remain valid
    until expiration. For immediate invalidation, implement token blacklisting.
    """
    # Clear refresh token cookie
    _clear_refresh_cookie(response)

    # Log logout event
    log_security_event(
        event_type="logout",
        user_id=str(current_user.id),
        ip_address=_get_client_ip(request),
        success=True,
    )

    return APIResponse(
        success=True,
        data=None,
        timestamp=datetime.now(timezone.utc),
    )
