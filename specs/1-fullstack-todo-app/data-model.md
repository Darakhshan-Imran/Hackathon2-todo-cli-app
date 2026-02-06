# Data Model: Full-Stack Todo Application

**Feature**: `1-fullstack-todo-app`
**Date**: 2026-02-05
**Phase**: 1 (Design)

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ENTITY RELATIONSHIPS                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│   ┌──────────────────────────┐          ┌──────────────────────────────┐    │
│   │          USER            │          │           TODO               │    │
│   ├──────────────────────────┤          ├──────────────────────────────┤    │
│   │ id: UUID (PK)            │──────────│ id: UUID (PK)                │    │
│   │ email: VARCHAR(255)      │  1    N  │ user_id: UUID (FK) ──────────│────┘
│   │ username: VARCHAR(30)    │──────────│ title: VARCHAR(255)          │
│   │ password_hash: VARCHAR   │          │ description: TEXT            │
│   │ created_at: TIMESTAMPTZ  │          │ status: TodoStatus           │
│   │ updated_at: TIMESTAMPTZ  │          │ priority: Priority           │
│   │ deleted_at: TIMESTAMPTZ  │          │ due_date: TIMESTAMPTZ        │
│   └──────────────────────────┘          │ tags: JSONB                  │
│                                         │ created_at: TIMESTAMPTZ      │
│                                         │ updated_at: TIMESTAMPTZ      │
│                                         │ deleted_at: TIMESTAMPTZ      │
│                                         └──────────────────────────────┘
│                                                                               │
│   Relationship: User 1:N Todo                                                 │
│   - A user can have zero or more todos                                        │
│   - A todo belongs to exactly one user                                        │
│   - Soft delete on user cascades to todos                                     │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Entity Definitions

### User

Represents an authenticated account holder in the system.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique identifier (uuid4) |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User's email address |
| username | VARCHAR(30) | UNIQUE, NOT NULL, INDEX | Display name |
| password_hash | VARCHAR | NOT NULL | Bcrypt hash (60 chars) |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMPTZ | NOT NULL, AUTO UPDATE | Last modification time |
| deleted_at | TIMESTAMPTZ | NULL | Soft delete timestamp |

**Validation Rules**:
- Email: Valid email format, max 255 chars, unique
- Username: 3-30 chars, alphanumeric + underscore only, unique
- Password (before hashing): min 8 chars, at least 1 uppercase, 1 lowercase, 1 number

**SQLModel Definition**:

```python
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    username: str = Field(max_length=30, unique=True, index=True)
    password_hash: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)
```

---

### Todo

Represents a task item belonging to a user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique identifier |
| user_id | UUID | FK → users.id, NOT NULL, INDEX | Owner reference |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULL | Detailed description |
| status | ENUM | NOT NULL, DEFAULT 'pending' | Current status |
| priority | ENUM | NOT NULL, DEFAULT 'medium' | Priority level |
| due_date | TIMESTAMPTZ | NULL | Optional deadline |
| tags | JSONB | DEFAULT '[]' | List of string tags |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMPTZ | NOT NULL, AUTO UPDATE | Last modification |
| deleted_at | TIMESTAMPTZ | NULL | Soft delete timestamp |

**Enums**:

```python
from enum import Enum

class TodoStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

**Validation Rules**:
- Title: Required, 1-255 chars
- Description: Optional, unlimited text
- Status: One of [pending, in_progress, completed]
- Priority: One of [low, medium, high]
- Tags: Array of strings, each tag max 50 chars

**SQLModel Definition**:

```python
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    status: TodoStatus = Field(default=TodoStatus.PENDING)
    priority: Priority = Field(default=Priority.MEDIUM)
    due_date: Optional[datetime] = Field(default=None)
    tags: List[str] = Field(default=[], sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)
```

---

## Database Indexes

```sql
-- Users table indexes
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Todos table indexes (partial indexes exclude soft-deleted records)
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_user_status ON todos(user_id, status) WHERE deleted_at IS NULL;
CREATE INDEX idx_todos_user_priority ON todos(user_id, priority) WHERE deleted_at IS NULL;
CREATE INDEX idx_todos_user_created ON todos(user_id, created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_todos_user_due_date ON todos(user_id, due_date)
    WHERE deleted_at IS NULL AND due_date IS NOT NULL;
```

---

## State Transitions

### Todo Status Transitions

```
┌─────────────┐
│   pending   │◄──────────────────────────────┐
└──────┬──────┘                               │
       │ start                                │ reopen
       ▼                                      │
┌─────────────┐                               │
│ in_progress │────────────────────────────────
└──────┬──────┘                               │
       │ complete                             │
       ▼                                      │
┌─────────────┐                               │
│  completed  │───────────────────────────────┘
└─────────────┘
```

**Allowed Transitions** (all directions permitted):
- pending → in_progress (start working)
- pending → completed (quick complete)
- in_progress → completed (finish)
- in_progress → pending (pause)
- completed → pending (reopen)
- completed → in_progress (resume work)

No business rules restrict status changes.

---

## Soft Delete Strategy

Both User and Todo implement soft delete via `deleted_at` timestamp:

1. **Delete Operation**: Sets `deleted_at = NOW()` instead of removing row
2. **Query Filter**: All normal queries include `WHERE deleted_at IS NULL`
3. **Retention Period**: 30 days before permanent deletion (future cleanup job)
4. **Cascade Behavior**: Deleting user should soft-delete all associated todos

**Query Pattern**:

```python
# Always exclude soft-deleted records in normal queries
async def get_todos(user_id: UUID, session: AsyncSession) -> list[Todo]:
    query = select(Todo).where(
        Todo.user_id == user_id,
        Todo.deleted_at.is_(None)  # Exclude soft-deleted
    )
    result = await session.execute(query)
    return result.scalars().all()
```

---

## Request/Response Schemas

### User Schemas

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    created_at: datetime

class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
```

### Todo Schemas

```python
class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: TodoStatus = TodoStatus.PENDING
    priority: Priority = Priority.MEDIUM
    due_date: datetime | None = None
    tags: list[str] = Field(default=[])

class TodoResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    status: TodoStatus
    priority: Priority
    due_date: datetime | None
    tags: list[str]
    created_at: datetime
    updated_at: datetime

class TodoUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: TodoStatus | None = None
    priority: Priority | None = None
    due_date: datetime | None = None
    tags: list[str] | None = None

class TodoListResponse(BaseModel):
    items: list[TodoResponse]
    page: int
    per_page: int
    total: int
    total_pages: int
```

### Auth Schemas

```python
class SignupRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

---

## API Response Wrapper

All responses wrapped in consistent format:

```python
from typing import TypeVar, Generic
from pydantic import BaseModel
from datetime import datetime

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Success example
APIResponse[TodoResponse](success=True, data=todo)

# Error example
APIResponse[None](success=False, error="Todo not found")

# Paginated example
class PaginatedData(BaseModel, Generic[T]):
    items: list[T]
    page: int
    per_page: int
    total: int
    total_pages: int

APIResponse[PaginatedData[TodoResponse]](success=True, data=paginated_todos)
```

---

## TypeScript Types (Frontend)

```typescript
// types/user.ts
export interface User {
  id: string;
  email: string;
  username: string;
  created_at: string;
}

export interface UserCreate {
  email: string;
  username: string;
  password: string;
}

// types/todo.ts
export type TodoStatus = 'pending' | 'in_progress' | 'completed';
export type Priority = 'low' | 'medium' | 'high';

export interface Todo {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  status: TodoStatus;
  priority: Priority;
  due_date: string | null;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface TodoCreate {
  title: string;
  description?: string;
  status?: TodoStatus;
  priority?: Priority;
  due_date?: string;
  tags?: string[];
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  status?: TodoStatus;
  priority?: Priority;
  due_date?: string;
  tags?: string[];
}

// types/api.ts
export interface APIResponse<T> {
  success: boolean;
  data: T | null;
  error: string | null;
  timestamp: string;
}

export interface PaginatedData<T> {
  items: T[];
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}
```
