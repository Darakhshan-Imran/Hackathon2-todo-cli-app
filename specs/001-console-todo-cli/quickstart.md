# Quickstart: Phase 1 Console Todo CLI

**Feature Branch**: `001-console-todo-cli`
**Date**: 2026-01-01

---

## Prerequisites

- Python 3.13 or higher
- uv package manager

---

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd todo-app

# Switch to feature branch
git checkout 001-console-todo-cli

# Install dependencies with uv
uv sync

# Install development dependencies
uv sync --extra dev
```

---

## Running the Application

```bash
# Start the todo CLI
uv run python -m src.main

# Or after installation
uv run todo
```

---

## Basic Usage

### Welcome Screen

When you start the application, you'll see:

```
Welcome to Todo CLI!
Type 'help' for available commands or 'exit' to quit.

todo>
```

### Creating Todos

```bash
# Add a todo with title only
todo> add "Buy groceries"
Todo 1 created: "Buy groceries"

# Add a todo with title and description
todo> add "Call mom" "Wish her happy birthday"
Todo 2 created: "Call mom"
```

### Viewing Todos

```bash
# List all todos
todo> list
ID  Title           Status       Description
──  ──────────────  ──────────  ────────────────────
1   Buy groceries   incomplete  (no description)
2   Call mom        incomplete  Wish her happy birthday

# Filter by status
todo> list --status incomplete
todo> list --status complete

# View single todo details
todo> show 1
Todo #1
───────────────────────────────
Title:       Buy groceries
Description: (no description)
Status:      incomplete
Created:     2026-01-01 12:00:00
```

### Managing Todos

```bash
# Mark as complete
todo> complete 1
Todo 1 marked as complete

# Mark as incomplete
todo> incomplete 1
Todo 1 marked as incomplete

# Update todo
todo> update 1 --title "Buy groceries today"
Todo 1 updated

todo> update 1 --description "Milk, eggs, bread"
Todo 1 updated

# Delete todo
todo> delete 2
Todo 2 deleted
```

### JSON Output

```bash
# Any command with --json flag
todo> list --json
{
  "success": true,
  "todos": [...],
  "count": 2
}

todo> show 1 --json
{
  "success": true,
  "todo": {...}
}
```

### Exiting

```bash
todo> exit
Goodbye!

# Or
todo> quit
Goodbye!
```

---

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Create a new todo | `add "Title" "Description"` |
| `list` | Show all todos | `list --status incomplete` |
| `show` | Show todo details | `show 1` |
| `complete` | Mark as complete | `complete 1` |
| `incomplete` | Mark as incomplete | `incomplete 1` |
| `update` | Update todo fields | `update 1 --title "New"` |
| `delete` | Remove a todo | `delete 1` |
| `help` | Show help | `help` |
| `exit` | Exit application | `exit` |

---

## Error Handling

```bash
# Invalid ID
todo> complete 99
Error: Todo with ID 99 not found

# Empty title
todo> add ""
Error: Title is required

# Non-numeric ID
todo> delete abc
Error: Invalid ID. ID must be a positive number

# Unknown command
todo> foo
Unknown command. Type 'help' for available commands
```

---

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_models.py
```

### Code Quality

```bash
# Lint code
uv run ruff check src tests

# Format code
uv run ruff format src tests

# Type checking
uv run mypy src
```

---

## Limitations (Phase 1)

- **In-memory storage**: All todos are lost when you exit
- **Single user**: No multi-user support
- **No persistence**: No file or database saving
- **English only**: No internationalization

These will be addressed in future phases.

---

## Next Steps

After completing Phase 1:

1. **Phase 2**: Add SQLite persistence and REST API
2. **Phase 3**: Add web UI and chatbot (English/Urdu)
3. **Phase 4**: Add voice commands and cloud deployment
