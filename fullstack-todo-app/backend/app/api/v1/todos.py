"""Todo CRUD endpoints."""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Query

from app.dependencies import CurrentUser, DbSession
from app.models.enums import Priority, TodoStatus
from app.models.schemas import (
    APIResponse,
    PaginatedData,
    TodoCreate,
    TodoResponse,
    TodoUpdate,
)
from app.services.todo_service import TodoService

router = APIRouter()


@router.get("")
async def list_todos(
    session: DbSession,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    status: TodoStatus | None = None,
    priority: Priority | None = None,
    due: str | None = Query(default=None, pattern=r"^(today|upcoming)$"),
    sort_by: str = Query(default="created_at", pattern=r"^(created_at|due_date|priority)$"),
    sort_order: str = Query(default="desc", pattern=r"^(asc|desc)$"),
) -> APIResponse[PaginatedData[TodoResponse]]:
    """
    List user's todos with filtering, sorting, and pagination.

    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    - status: Filter by status (pending, in_progress, completed)
    - priority: Filter by priority (low, medium, high)
    - due: Filter by due date (today, upcoming)
    - sort_by: Sort field (created_at, due_date, priority)
    - sort_order: Sort direction (asc, desc)
    """
    todo_service = TodoService(session)
    paginated_data = await todo_service.list_todos(
        user_id=current_user.id,
        page=page,
        per_page=per_page,
        status=status,
        priority=priority,
        due=due,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return APIResponse(
        success=True,
        data=paginated_data,
        timestamp=datetime.now(timezone.utc),
    )


@router.post("", status_code=201)
async def create_todo(
    data: TodoCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> APIResponse[TodoResponse]:
    """
    Create a new todo.

    Default values:
    - status: pending
    - priority: medium
    """
    todo_service = TodoService(session)
    todo = await todo_service.create_todo(
        user_id=current_user.id,
        data=data,
    )

    return APIResponse(
        success=True,
        data=TodoResponse.model_validate(todo),
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/{todo_id}")
async def get_todo(
    todo_id: UUID,
    session: DbSession,
    current_user: CurrentUser,
) -> APIResponse[TodoResponse]:
    """
    Get a single todo by ID.

    Returns 404 if todo not found or not owned by user.
    """
    todo_service = TodoService(session)
    todo = await todo_service.get_todo(
        todo_id=todo_id,
        user_id=current_user.id,
    )

    return APIResponse(
        success=True,
        data=TodoResponse.model_validate(todo),
        timestamp=datetime.now(timezone.utc),
    )


@router.patch("/{todo_id}")
async def update_todo(
    todo_id: UUID,
    data: TodoUpdate,
    session: DbSession,
    current_user: CurrentUser,
) -> APIResponse[TodoResponse]:
    """
    Update a todo (partial update).

    Only provided fields will be updated.
    Returns 404 if todo not found or not owned by user.
    """
    todo_service = TodoService(session)
    todo = await todo_service.update_todo(
        todo_id=todo_id,
        user_id=current_user.id,
        data=data,
    )

    return APIResponse(
        success=True,
        data=TodoResponse.model_validate(todo),
        timestamp=datetime.now(timezone.utc),
    )


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: UUID,
    session: DbSession,
    current_user: CurrentUser,
) -> APIResponse[None]:
    """
    Soft delete a todo.

    The todo is marked as deleted but retained for 30 days.
    Returns 404 if todo not found or not owned by user.
    """
    todo_service = TodoService(session)
    await todo_service.soft_delete_todo(
        todo_id=todo_id,
        user_id=current_user.id,
    )

    return APIResponse(
        success=True,
        data=None,
        timestamp=datetime.now(timezone.utc),
    )
