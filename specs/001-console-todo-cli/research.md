# Research: Phase 1 Console Todo CLI

**Feature Branch**: `001-console-todo-cli`
**Date**: 2026-01-01
**Status**: Complete

## Research Summary

This document captures technology decisions and best practices research for the Phase 1 Console Todo CLI application.

---

## Technology Decisions

### 1. CLI Framework Selection

**Decision**: Use Python's built-in `argparse` module

**Rationale**:
- Zero external dependencies (per Constitution XIII: Simplicity)
- Built into Python standard library since 3.2
- Supports subcommands, arguments, and flags natively
- Sufficient for Phase 1 requirements
- Easy migration to Click or Typer in future phases if needed

**Alternatives Considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Click | Decorators, great DX | External dependency | Unnecessary complexity for Phase 1 |
| Typer | Type hints, auto-complete | Requires Click | Two dependencies for simple CLI |
| cmd module | Built-in, REPL style | Less intuitive command parsing | Not ideal for one-shot commands |

---

### 2. Data Structure for Todos

**Decision**: Use Python `dataclass` with `dict` storage

**Rationale**:
- `dataclass` provides type hints, `__repr__`, `__eq__` automatically
- Dict provides O(1) lookup by ID
- Immutable fields (ID, created_at) can be enforced with `frozen=False` and property
- Easy serialization to JSON for `--json` flag
- Simple migration to ORM models in Phase 2

**Alternatives Considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Plain dict | Simplest | No type safety | Harder to maintain, refactor |
| NamedTuple | Immutable, typed | Immutable (hard to update) | Need mutable status field |
| Pydantic | Validation built-in | External dependency | Over-engineered for Phase 1 |
| attrs | Similar to dataclass | External dependency | dataclass is built-in |

---

### 3. ID Generation Strategy

**Decision**: Sequential integer starting from 1, stored in memory counter

**Rationale**:
- Simplest approach for in-memory storage
- User-friendly (easy to type `complete 1`)
- Clear ordering (first todo is always ID 1)
- Easy to migrate to UUID in Phase 2+ (swap generator, update type hints)

**Implementation**:
```python
class TodoStore:
    _next_id: int = 1

    def _generate_id(self) -> int:
        id = self._next_id
        self._next_id += 1
        return id
```

---

### 4. Input Parsing Strategy

**Decision**: Use `shlex.split()` for command parsing with argparse subparsers

**Rationale**:
- `shlex.split()` handles quoted strings correctly: `add "Buy groceries" "Milk, eggs"`
- Argparse subparsers map to commands (add, list, complete, etc.)
- Built-in error handling and help generation
- Consistent with Unix command-line conventions

**Example Flow**:
```
User: add "Buy groceries" "Milk, eggs"
↓ shlex.split()
['add', 'Buy groceries', 'Milk, eggs']
↓ argparse
Namespace(command='add', title='Buy groceries', description='Milk, eggs')
```

---

### 5. Output Formatting

**Decision**: Rich-text tables for human output, `json.dumps()` for JSON

**Rationale**:
- Human output: Simple formatted strings with consistent widths
- JSON output: Standard library `json` module with indentation
- Dual-format satisfies Constitution XII (Observability)
- No external dependencies needed

**Output Modes**:
- Default: Human-readable table format
- `--json`: Machine-readable JSON

---

### 6. Error Handling Strategy

**Decision**: Custom exception hierarchy with user-friendly messages

**Rationale**:
- Consistent error format across all commands
- Separation between user errors (invalid ID) and system errors
- Never expose stack traces to users
- Log full errors in debug mode only

**Exception Hierarchy**:
```
TodoError (base)
├── TodoNotFoundError
├── ValidationError
│   ├── EmptyTitleError
│   └── InvalidIdError
└── CommandError
```

---

### 7. Testing Strategy

**Decision**: pytest with fixtures for todo store setup

**Rationale**:
- pytest is Constitution-mandated (Technology Stack)
- Fixtures enable clean test isolation
- Parametrized tests for edge cases
- Easy mocking for CLI input/output testing

**Test Structure**:
```
tests/
├── unit/
│   ├── test_models.py      # Todo dataclass tests
│   ├── test_store.py       # TodoStore CRUD tests
│   └── test_validators.py  # Input validation tests
├── integration/
│   └── test_cli.py         # End-to-end CLI tests
└── conftest.py             # Shared fixtures
```

---

### 8. Project Structure

**Decision**: Single project with layered architecture

**Rationale**:
- Simplest structure that supports separation of concerns
- Clear boundaries: CLI → Service → Store → Model
- Easy to extract service layer for API in Phase 2
- Follows Constitution V (Clean Code Architecture)

**Layers**:
```
CLI Layer (src/cli/)
    ↓ calls
Service Layer (src/services/)
    ↓ uses
Store Layer (src/store/)
    ↓ manages
Model Layer (src/models/)
```

---

## Best Practices Applied

### Python Best Practices

1. **Type Hints**: All functions annotated with types (Constitution XI requirement)
2. **Docstrings**: Google-style docstrings for public functions
3. **Constants**: Magic strings/numbers extracted to constants module
4. **Enums**: Status values as Enum for type safety

### CLI Best Practices

1. **Exit Codes**: 0 for success, 1 for user error, 2 for system error
2. **Help Text**: Every command has `-h/--help` with examples
3. **Consistent Syntax**: All commands follow `command [args] [--flags]` pattern
4. **Error Messages**: Start with context, end with suggestion

### Testing Best Practices

1. **Arrange-Act-Assert**: Clear test structure
2. **One Assertion Per Test**: Focused tests (where practical)
3. **Descriptive Names**: `test_add_todo_with_empty_title_raises_validation_error`
4. **Fixtures Over Setup**: pytest fixtures for reusable state

---

## Phase 2+ Migration Considerations

### Preparation for Persistence (Phase 2)

| Phase 1 Component | Migration Path |
|-------------------|----------------|
| In-memory dict | Replace with SQLAlchemy session |
| Sequential ID | Replace with UUID generator |
| TodoStore class | Implement Repository pattern |
| Direct store access | Add Unit of Work pattern |

### Preparation for API (Phase 2)

| Phase 1 Component | Migration Path |
|-------------------|----------------|
| CLI commands | Map to FastAPI routes |
| Service methods | Reuse directly (no change) |
| JSON output | Return as response body |
| Error exceptions | Map to HTTP status codes |

### Preparation for Chatbot (Phase 3)

| Phase 1 Component | Migration Path |
|-------------------|----------------|
| Command names | Natural language intent mapping |
| Structured output | Response templates |
| Validation errors | User-friendly rephrasing |

---

## Unresolved Items

None. All technical decisions are finalized for Phase 1.

---

## References

- Python argparse documentation: https://docs.python.org/3/library/argparse.html
- Python dataclasses: https://docs.python.org/3/library/dataclasses.html
- pytest best practices: https://docs.pytest.org/en/stable/explanation/goodpractices.html
- Constitution v1.0.0: `.specify/memory/constitution.md`
