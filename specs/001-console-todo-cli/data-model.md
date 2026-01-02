# Data Model: Phase 1 Console Todo CLI

**Feature Branch**: `001-console-todo-cli`
**Date**: 2026-01-01
**Status**: Complete

---

## Entity Definitions

### Todo

The primary entity representing a task to be completed.

```
┌─────────────────────────────────────────────────────┐
│                       Todo                          │
├─────────────────────────────────────────────────────┤
│ id: int [PK, auto-generated, immutable]             │
│ title: str [required, 1-200 chars]                  │
│ description: str [optional, default: ""]            │
│ status: TodoStatus [default: INCOMPLETE]            │
│ created_at: datetime [auto-generated, immutable]    │
└─────────────────────────────────────────────────────┘
```

#### Field Specifications

| Field | Type | Constraints | Default | Mutable |
|-------|------|-------------|---------|---------|
| `id` | `int` | Positive integer, unique, sequential | Auto-generated | No |
| `title` | `str` | Non-empty, max 200 chars | Required | Yes |
| `description` | `str` | Any length | `""` (empty) | Yes |
| `status` | `TodoStatus` | Enum value | `INCOMPLETE` | Yes |
| `created_at` | `datetime` | UTC timestamp | Current time | No |

---

### TodoStatus (Enum)

Represents the completion state of a todo.

```
┌──────────────────────────┐
│       TodoStatus         │
├──────────────────────────┤
│ INCOMPLETE = "incomplete"│
│ COMPLETE = "complete"    │
└──────────────────────────┘
```

---

## State Transitions

```
                    ┌─────────────┐
                    │  [Created]  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
         ┌──────────│ INCOMPLETE  │◄─────────┐
         │          └──────┬──────┘          │
         │                 │                 │
         │    complete(id) │    incomplete(id)
         │                 │                 │
         │                 ▼                 │
         │          ┌─────────────┐          │
         │          │  COMPLETE   │──────────┘
         │          └──────┬──────┘
         │                 │
         │    delete(id)   │    delete(id)
         │                 │
         └────────►┌───────▼───────┐◄────────┘
                   │   [Deleted]   │
                   └───────────────┘
```

---

## Validation Rules

### Title Validation

| Rule | Condition | Error Message |
|------|-----------|---------------|
| Required | `len(title.strip()) > 0` | "Title is required" |
| Max Length | `len(title) <= 200` | "Title must be 200 characters or less" |

### ID Validation

| Rule | Condition | Error Message |
|------|-----------|---------------|
| Numeric | `isinstance(id, int)` | "Invalid ID. ID must be a positive number" |
| Positive | `id > 0` | "Invalid ID. ID must be a positive number" |
| Exists | `id in store` | "Todo with ID {id} not found" |

### Status Validation

| Rule | Condition | Error Message |
|------|-----------|---------------|
| Valid Value | `status in TodoStatus` | "Invalid status. Use 'complete' or 'incomplete'" |

---

## Data Operations

### Create (add)

```
Input:  title: str, description: str = ""
Output: Todo
Side Effects:
  - Assigns next sequential ID
  - Sets created_at to current UTC time
  - Sets status to INCOMPLETE
  - Stores in memory
```

### Read (list, show)

```
# List all
Input:  status_filter: Optional[TodoStatus] = None
Output: List[Todo]

# Show one
Input:  id: int
Output: Todo
Raises: TodoNotFoundError if id not found
```

### Update

```
Input:  id: int, title: Optional[str], description: Optional[str]
Output: Todo
Raises:
  - TodoNotFoundError if id not found
  - ValidationError if no fields provided
  - ValidationError if title is empty
```

### Delete

```
Input:  id: int
Output: None
Raises: TodoNotFoundError if id not found
Side Effects: Removes todo from memory store
```

### Status Change (complete, incomplete)

```
Input:  id: int
Output: Todo
Raises: TodoNotFoundError if id not found
Side Effects: Updates status field
```

---

## Storage Model

### In-Memory Store (Phase 1)

```
TodoStore
├── _todos: Dict[int, Todo]  # ID → Todo mapping
├── _next_id: int            # Counter for ID generation
│
├── add(title, description) → Todo
├── get(id) → Todo
├── get_all(status_filter) → List[Todo]
├── update(id, title, description) → Todo
├── delete(id) → None
├── mark_complete(id) → Todo
└── mark_incomplete(id) → Todo
```

### Future Persistence Model (Phase 2)

The in-memory store will be replaced with a repository pattern:

```
# Phase 2 migration
TodoRepository (interface)
├── save(todo) → Todo
├── find_by_id(id) → Optional[Todo]
├── find_all(filter) → List[Todo]
├── delete(id) → None
│
SQLAlchemyTodoRepository (implementation)
└── Uses SQLAlchemy ORM with Session
```

---

## Serialization

### JSON Output Format

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "incomplete",
  "created_at": "2026-01-01T12:00:00Z"
}
```

### List Output Format

```json
{
  "todos": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "status": "incomplete",
      "created_at": "2026-01-01T12:00:00Z"
    }
  ],
  "count": 1
}
```

### Error Output Format

```json
{
  "error": true,
  "message": "Todo with ID 99 not found",
  "code": "TODO_NOT_FOUND"
}
```

---

## Index Strategy

### Phase 1 (In-Memory)

- **Primary Index**: `Dict[int, Todo]` - O(1) lookup by ID
- **No Secondary Indexes**: Full scan for filtering (acceptable for <1000 items)

### Phase 2+ (Database)

| Index | Column(s) | Purpose |
|-------|-----------|---------|
| PK | `id` | Primary lookup |
| IDX_STATUS | `status` | Filter by completion status |
| IDX_CREATED | `created_at` | Sort by creation time |

---

## Migration Path

### Phase 1 → Phase 2 (Add Persistence)

1. Create SQLAlchemy model mirroring `Todo` dataclass
2. Implement `TodoRepository` interface
3. Replace `TodoStore` with `SQLAlchemyTodoRepository`
4. Add database migration scripts
5. Change ID from `int` to `UUID` (optional)

### Phase 2 → Phase 3 (Add API)

1. Serialize/deserialize through Pydantic schemas
2. Map data operations to API endpoints
3. Add pagination to list operations
