# CLI Contract: Phase 1 Console Todo CLI

**Feature Branch**: `001-console-todo-cli`
**Date**: 2026-01-01
**Status**: Complete

---

## Command Contracts

This document defines the input/output contracts for all CLI commands in Phase 1.

---

### add

Create a new todo item.

**Syntax**:
```
add "<title>" ["<description>"]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| title | string | Yes | Todo title (1-200 chars) |
| description | string | No | Detailed description (default: "") |

**Success Output** (exit code 0):
```
Human: Todo 1 created: "Buy groceries"

JSON:
{
  "success": true,
  "todo": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "incomplete",
    "created_at": "2026-01-01T12:00:00Z"
  }
}
```

**Error Output** (exit code 1):
```
Human: Error: Title is required

JSON:
{
  "error": true,
  "message": "Title is required",
  "code": "VALIDATION_ERROR"
}
```

---

### list

Display all todos, optionally filtered by status.

**Syntax**:
```
list [--status <complete|incomplete>] [--json]
```

**Flags**:

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| --status | enum | No | Filter by status |
| --json | boolean | No | Output as JSON |

**Success Output** (exit code 0):
```
Human:
ID  Title                Status       Description
──  ────────────────────  ──────────  ────────────────────
1   Buy groceries         incomplete  Milk, eggs, bread
2   Call mom              complete    (no description)

JSON:
{
  "success": true,
  "todos": [...],
  "count": 2
}
```

**Empty Output** (exit code 0):
```
Human: No todos found. Use 'add' command to create one.

JSON:
{
  "success": true,
  "todos": [],
  "count": 0
}
```

---

### show

Display full details of a specific todo.

**Syntax**:
```
show <id> [--json]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| id | integer | Yes | Todo ID |

**Success Output** (exit code 0):
```
Human:
Todo #1
───────────────────────────────
Title:       Buy groceries
Description: Milk, eggs, bread
Status:      incomplete
Created:     2026-01-01 12:00:00

JSON:
{
  "success": true,
  "todo": {...}
}
```

**Error Output** (exit code 1):
```
Human: Error: Todo with ID 99 not found

JSON:
{
  "error": true,
  "message": "Todo with ID 99 not found",
  "code": "TODO_NOT_FOUND"
}
```

---

### complete

Mark a todo as complete.

**Syntax**:
```
complete <id> [--json]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| id | integer | Yes | Todo ID |

**Success Output** (exit code 0):
```
Human: Todo 1 marked as complete

JSON:
{
  "success": true,
  "todo": {...},
  "message": "Todo 1 marked as complete"
}
```

**Error Output** (exit code 1):
```
Human: Error: Todo with ID 99 not found

JSON:
{
  "error": true,
  "message": "Todo with ID 99 not found",
  "code": "TODO_NOT_FOUND"
}
```

---

### incomplete

Mark a todo as incomplete.

**Syntax**:
```
incomplete <id> [--json]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| id | integer | Yes | Todo ID |

**Success Output** (exit code 0):
```
Human: Todo 1 marked as incomplete

JSON:
{
  "success": true,
  "todo": {...},
  "message": "Todo 1 marked as incomplete"
}
```

**Error Output** (exit code 1):
```
Human: Error: Todo with ID 99 not found

JSON:
{
  "error": true,
  "message": "Todo with ID 99 not found",
  "code": "TODO_NOT_FOUND"
}
```

---

### update

Update a todo's title and/or description.

**Syntax**:
```
update <id> [--title "<new_title>"] [--description "<new_description>"] [--json]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| id | integer | Yes | Todo ID |

**Flags**:

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| --title | string | No | New title |
| --description | string | No | New description |
| --json | boolean | No | Output as JSON |

**Validation**: At least one of `--title` or `--description` must be provided.

**Success Output** (exit code 0):
```
Human: Todo 1 updated

JSON:
{
  "success": true,
  "todo": {...},
  "message": "Todo 1 updated"
}
```

**Error Output** (exit code 1):
```
Human: Error: Specify --title or --description to update

JSON:
{
  "error": true,
  "message": "Specify --title or --description to update",
  "code": "VALIDATION_ERROR"
}
```

---

### delete

Remove a todo permanently.

**Syntax**:
```
delete <id> [--json]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| id | integer | Yes | Todo ID |

**Success Output** (exit code 0):
```
Human: Todo 1 deleted

JSON:
{
  "success": true,
  "message": "Todo 1 deleted"
}
```

**Error Output** (exit code 1):
```
Human: Error: Todo with ID 99 not found

JSON:
{
  "error": true,
  "message": "Todo with ID 99 not found",
  "code": "TODO_NOT_FOUND"
}
```

---

### help

Display available commands and usage.

**Syntax**:
```
help
```

**Output** (exit code 0):
```
Todo CLI - In-Memory Task Manager

Commands:
  add "<title>" ["<description>"]     Create a new todo
  list [--status <status>]            Show all todos
  show <id>                           Show todo details
  complete <id>                       Mark as complete
  incomplete <id>                     Mark as incomplete
  update <id> [--title] [--desc]      Update todo fields
  delete <id>                         Remove a todo
  help                                Show this message
  exit                                Exit the application

Global Flags:
  --json                              Output as JSON

Examples:
  add "Buy groceries" "Milk, eggs"
  list --status incomplete
  complete 1
  update 1 --title "New title"
```

---

### exit / quit

Terminate the application.

**Syntax**:
```
exit
quit
```

**Output** (exit code 0):
```
Human: Goodbye!

JSON:
{
  "success": true,
  "message": "Session ended"
}
```

---

## Error Codes

| Code | HTTP Equivalent | Description |
|------|-----------------|-------------|
| TODO_NOT_FOUND | 404 | Todo with specified ID does not exist |
| VALIDATION_ERROR | 400 | Input validation failed |
| INVALID_ID | 400 | ID is not a valid positive integer |
| COMMAND_ERROR | 400 | Unknown or malformed command |
| SYSTEM_ERROR | 500 | Unexpected internal error |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | User/validation error |
| 2 | System error |

---

## Future API Mapping (Phase 2)

| CLI Command | HTTP Method | Endpoint |
|-------------|-------------|----------|
| add | POST | /api/todos |
| list | GET | /api/todos |
| show | GET | /api/todos/{id} |
| complete | PATCH | /api/todos/{id}/complete |
| incomplete | PATCH | /api/todos/{id}/incomplete |
| update | PATCH | /api/todos/{id} |
| delete | DELETE | /api/todos/{id} |
