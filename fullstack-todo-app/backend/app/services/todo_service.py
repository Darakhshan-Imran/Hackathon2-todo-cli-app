"""Todo service for CRUD operations with user isolation."""

from datetime import date, datetime, time, timezone
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.enums import Priority, TodoStatus
from app.models.schemas import PaginatedData, TodoCreate, TodoResponse, TodoUpdate
from app.models.todo import Todo
from app.utils.auto_tags import extract_tags
from app.utils.exceptions import NotFoundError


class TodoService:
    """Service for todo operations with strict user isolation."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def create_todo(self, user_id: UUID, data: TodoCreate) -> Todo:
        """
        Create a new todo for a user.

        Args:
            user_id: Owner's user ID
            data: Todo creation data

        Returns:
            Created todo
        """
        tags = extract_tags(data.title, data.description)
        todo = Todo(
            user_id=user_id,
            title=data.title,
            description=data.description,
            status=data.status,
            priority=data.priority,
            due_date=data.due_date,
            tags=tags,
        )

        self.session.add(todo)
        await self.session.flush()
        await self.session.refresh(todo)

        return todo

    async def get_todo(self, todo_id: UUID, user_id: UUID) -> Todo:
        """
        Get a todo by ID, ensuring user ownership.

        Args:
            todo_id: Todo's unique identifier
            user_id: User ID for ownership verification

        Returns:
            Todo if found and owned by user

        Raises:
            NotFoundError: If todo not found or not owned by user
        """
        query = select(Todo).where(
            Todo.id == todo_id,
            Todo.user_id == user_id,  # User isolation
            Todo.deleted_at.is_(None),  # Exclude soft-deleted
        )
        result = await self.session.execute(query)
        todo = result.scalar_one_or_none()

        if not todo:
            # Return 404 for both not-found and not-owned (prevent enumeration)
            raise NotFoundError("Todo not found")

        return todo

    async def list_todos(
        self,
        user_id: UUID,
        page: int = 1,
        per_page: int = 20,
        status: TodoStatus | None = None,
        priority: Priority | None = None,
        due: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> PaginatedData[TodoResponse]:
        """
        List todos for a user with filtering, sorting, and pagination.

        Args:
            user_id: User ID for filtering
            page: Page number (1-indexed)
            per_page: Items per page
            status: Optional status filter
            priority: Optional priority filter
            due: Optional due date filter ("today" or "upcoming")
            sort_by: Sort field (created_at, due_date, priority)
            sort_order: Sort direction (asc, desc)

        Returns:
            Paginated todo list
        """
        # Base query with user isolation and soft-delete exclusion
        base_query = select(Todo).where(
            Todo.user_id == user_id,
            Todo.deleted_at.is_(None),
        )

        # Apply filters
        if status:
            base_query = base_query.where(Todo.status == status)
        if priority:
            base_query = base_query.where(Todo.priority == priority)
        if due == "today":
            today_start = datetime.combine(date.today(), time.min, tzinfo=timezone.utc)
            today_end = datetime.combine(date.today(), time.max, tzinfo=timezone.utc)
            base_query = base_query.where(
                Todo.due_date.isnot(None),
                Todo.due_date >= today_start,
                Todo.due_date <= today_end,
            )
        elif due == "upcoming":
            today_end = datetime.combine(date.today(), time.max, tzinfo=timezone.utc)
            base_query = base_query.where(
                Todo.due_date.isnot(None),
                Todo.due_date > today_end,
            )

        # Get total count
        count_query = select(func.count()).select_from(base_query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        # Apply sorting
        sort_column = getattr(Todo, sort_by, Todo.created_at)
        if sort_order == "desc":
            base_query = base_query.order_by(sort_column.desc())
        else:
            base_query = base_query.order_by(sort_column.asc())

        # Apply pagination
        offset = (page - 1) * per_page
        base_query = base_query.offset(offset).limit(per_page)

        # Execute query
        result = await self.session.execute(base_query)
        todos = result.scalars().all()

        # Calculate total pages
        total_pages = (total + per_page - 1) // per_page if total > 0 else 0

        return PaginatedData(
            items=[TodoResponse.model_validate(todo) for todo in todos],
            page=page,
            per_page=per_page,
            total=total,
            total_pages=total_pages,
        )

    async def update_todo(
        self,
        todo_id: UUID,
        user_id: UUID,
        data: TodoUpdate,
    ) -> Todo:
        """
        Update a todo, ensuring user ownership.

        Args:
            todo_id: Todo's unique identifier
            user_id: User ID for ownership verification
            data: Update data (partial)

        Returns:
            Updated todo

        Raises:
            NotFoundError: If todo not found or not owned by user
        """
        todo = await self.get_todo(todo_id, user_id)

        # Update only provided fields
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)

        # Regenerate tags if title or description changed
        if "title" in update_data or "description" in update_data:
            todo.tags = extract_tags(todo.title, todo.description)

        # Update timestamp
        todo.updated_at = datetime.now(timezone.utc)

        await self.session.flush()
        await self.session.refresh(todo)

        return todo

    async def soft_delete_todo(self, todo_id: UUID, user_id: UUID) -> None:
        """
        Soft delete a todo, ensuring user ownership.

        Args:
            todo_id: Todo's unique identifier
            user_id: User ID for ownership verification

        Raises:
            NotFoundError: If todo not found or not owned by user
        """
        todo = await self.get_todo(todo_id, user_id)

        # Set deleted_at timestamp (soft delete)
        todo.deleted_at = datetime.now(timezone.utc)

        await self.session.flush()
