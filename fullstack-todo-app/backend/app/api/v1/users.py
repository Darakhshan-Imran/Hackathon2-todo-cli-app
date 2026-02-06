"""User profile endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.dependencies import CurrentUser, DbSession
from app.models.schemas import APIResponse, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me")
async def get_current_user_profile(
    current_user: CurrentUser,
) -> APIResponse[UserResponse]:
    """
    Get current user's profile.

    Returns email, username, and creation date.
    """
    return APIResponse(
        success=True,
        data=UserResponse.model_validate(current_user),
        timestamp=datetime.now(timezone.utc),
    )


@router.patch("/me")
async def update_current_user_profile(
    data: UserUpdate,
    session: DbSession,
    current_user: CurrentUser,
) -> APIResponse[UserResponse]:
    """
    Update current user's profile.

    Only username can be updated. Email changes are not allowed.
    Returns 409 if username is already taken.
    """
    user_service = UserService(session)

    # Only update if username is provided
    if data.username:
        updated_user = await user_service.update_username(
            user_id=current_user.id,
            new_username=data.username,
        )
    else:
        updated_user = current_user

    return APIResponse(
        success=True,
        data=UserResponse.model_validate(updated_user),
        timestamp=datetime.now(timezone.utc),
    )
