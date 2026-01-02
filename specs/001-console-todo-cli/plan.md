# Implementation Plan: Phase 1 Console Todo CLI

**Branch**: `001-console-todo-cli` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-console-todo-cli/spec.md`

---

## Summary

Implement a command-line todo application in Python 3.13+ that provides CRUD operations for task management with in-memory storage. The application follows a layered architecture (CLI → Service → Store → Model) designed for future extensibility to API, persistence, and cloud-native patterns.

---

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only: argparse, dataclasses, datetime, json, shlex)
**Storage**: In-memory (dict with dataclass values)
**Testing**: pytest
**Target Platform**: Cross-platform (Windows, macOS, Linux terminals)
**Project Type**: Single CLI application
**Performance Goals**: <1 second response for all commands, support 1000+ todos
**Constraints**: No file I/O, no database, no external dependencies for core functionality
**Scale/Scope**: Single user, session-based storage

---

## Constitution Check

*GATE: Must pass before implementation. All items verified against Constitution v1.0.0*

| Principle | Requirement | Status |
|-----------|-------------|--------|
| I. Spec-Driven Development | Specification exists before implementation | ✅ PASS |
| II. Reusable Intelligence | Subagents and Agent Skills defined | ✅ PASS |
| III. Cloud-Native Blueprints | Future mappings declared in spec | ✅ PASS |
| IV. Python Standards | Python 3.13+, uv package manager | ✅ PASS |
| V. Clean Code | Layered architecture, single responsibility | ✅ PASS |
| VI. Phase 1 Storage | In-memory only, no persistence | ✅ PASS |
| VII. Language Standards | English interface | ✅ PASS |
| VIII. Voice Command | Declared but not implemented | ✅ PASS |
| IX. Modular Extensibility | Business logic separate from I/O | ✅ PASS |
| X. Security-First | Input validation at all entry points | ✅ PASS |
| XI. Test-First | TDD with pytest, 80% coverage target | ✅ PASS |
| XII. Observability | JSON output flag, structured errors | ✅ PASS |
| XIII. Simplicity | Minimal dependencies, YAGNI applied | ✅ PASS |

**Gate Result**: ✅ ALL PASSED - Proceed with implementation

---

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo-cli/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Technology decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Usage guide
├── contracts/
│   └── cli-contract.md  # CLI input/output contracts
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Implementation tasks (next phase)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py              # Entry point, REPL loop
├── models/
│   ├── __init__.py
│   ├── todo.py          # Todo dataclass
│   └── status.py        # TodoStatus enum
├── store/
│   ├── __init__.py
│   └── todo_store.py    # In-memory storage
├── services/
│   ├── __init__.py
│   └── todo_service.py  # Business logic
├── cli/
│   ├── __init__.py
│   ├── parser.py        # Argparse configuration
│   ├── commands.py      # Command handlers
│   └── formatters.py    # Output formatting
├── exceptions/
│   ├── __init__.py
│   └── errors.py        # Custom exceptions
└── utils/
    ├── __init__.py
    └── validators.py    # Input validation

tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── unit/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_store.py
│   ├── test_service.py
│   └── test_validators.py
└── integration/
    ├── __init__.py
    └── test_cli.py
```

**Structure Decision**: Single project with layered architecture. CLI layer handles parsing/formatting, Service layer contains business logic, Store layer manages data, Models define entities. This separation enables easy extraction of Service layer for API in Phase 2.

---

## Component Design

### Layer Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Layer                            │
│  parser.py: argparse setup, command routing                 │
│  commands.py: handle commands, call service                 │
│  formatters.py: human-readable & JSON output                │
└─────────────────────────┬───────────────────────────────────┘
                          │ calls
┌─────────────────────────▼───────────────────────────────────┐
│                      Service Layer                          │
│  todo_service.py: business logic, validation orchestration  │
│  - create_todo(title, description)                          │
│  - get_todo(id) / get_all_todos(filter)                     │
│  - update_todo(id, fields)                                  │
│  - delete_todo(id)                                          │
│  - complete_todo(id) / incomplete_todo(id)                  │
└─────────────────────────┬───────────────────────────────────┘
                          │ uses
┌─────────────────────────▼───────────────────────────────────┐
│                       Store Layer                           │
│  todo_store.py: in-memory CRUD operations                   │
│  - add(todo) → Todo                                         │
│  - get(id) → Optional[Todo]                                 │
│  - get_all() → List[Todo]                                   │
│  - update(id, updates) → Todo                               │
│  - delete(id) → None                                        │
└─────────────────────────┬───────────────────────────────────┘
                          │ manages
┌─────────────────────────▼───────────────────────────────────┐
│                      Model Layer                            │
│  todo.py: Todo dataclass                                    │
│  status.py: TodoStatus enum                                 │
│  errors.py: TodoError, TodoNotFoundError, ValidationError   │
└─────────────────────────────────────────────────────────────┘
```

### Phase 1 vs Future Reusable Components

| Component | Phase 1 Only | Future Reusable |
|-----------|--------------|-----------------|
| `Todo` dataclass | - | ✅ Becomes ORM model |
| `TodoStatus` enum | - | ✅ Reused across phases |
| `TodoStore` | ✅ (in-memory) | Replaced by Repository |
| `TodoService` | - | ✅ Core business logic |
| `validators.py` | - | ✅ Validation rules |
| `cli/parser.py` | ✅ (CLI-specific) | - |
| `cli/formatters.py` | Partial | JSON formatter reused |
| `exceptions/` | - | ✅ Error types |

---

## Subagent Assignments

Per Constitution Principle II, the following Subagents are assigned:

| Subagent | Responsibility | Applied To |
|----------|----------------|------------|
| Domain Logic Agent | Todo CRUD operations | `services/todo_service.py`, `store/todo_store.py` |
| Spec Validation Agent | Ensure code matches spec | All implementation |
| Code Quality Agent | Clean code standards | All files |
| Test Generation Agent | Generate test cases | `tests/` directory |

---

## Agent Skills Application

| Skill | Application in Phase 1 | Reuse in Phase 2+ |
|-------|------------------------|-------------------|
| `todo.domain` | CRUD in TodoService | Same service, different store |
| `todo.validate` | validators.py | Same validators |
| `spec.validate` | Verify against spec.md | Continue verification |
| `code.structure` | Layer separation | Add API layer |
| `code.quality` | ruff, mypy checks | Same tooling |
| `cloud.blueprint` | Declared in spec | Implement deployments |

---

## Cloud-Native Mapping (Phase 2+)

| Phase 1 Component | Cloud-Native Equivalent |
|-------------------|------------------------|
| `TodoService` methods | Lambda/Cloud Functions |
| `TodoStore` | DynamoDB Table / PostgreSQL |
| CLI commands | API Gateway endpoints |
| In-memory dict | Managed database service |
| JSON formatters | API response schemas |
| Exit codes | HTTP status codes |

### Event Mapping for Future

| Phase 1 Action | Future Event |
|----------------|--------------|
| `create_todo()` | Publish `todo.created` to EventBridge/SNS |
| `complete_todo()` | Publish `todo.status.changed` |
| `delete_todo()` | Publish `todo.deleted` |

---

## Dependencies

### Runtime (Phase 1)

```toml
# pyproject.toml - No external runtime dependencies
[project]
dependencies = []
```

### Development

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
]
```

---

## Testing Strategy

### Test Coverage Targets

| Layer | Target | Test Type |
|-------|--------|-----------|
| Models | 100% | Unit |
| Store | 100% | Unit |
| Service | 95% | Unit |
| Validators | 100% | Unit |
| CLI | 90% | Integration |
| **Overall** | **80%+** | Mixed |

### Test Structure

```
tests/
├── conftest.py          # Fixtures: empty_store, store_with_todos
├── unit/
│   ├── test_models.py   # Todo, TodoStatus tests
│   ├── test_store.py    # TodoStore CRUD tests
│   ├── test_service.py  # TodoService logic tests
│   └── test_validators.py
└── integration/
    └── test_cli.py      # Full command flow tests
```

---

## Implementation Order

1. **Models** → Foundation types (Todo, TodoStatus, Exceptions)
2. **Store** → In-memory CRUD operations
3. **Validators** → Input validation functions
4. **Service** → Business logic orchestration
5. **CLI Parser** → Argparse configuration
6. **CLI Commands** → Command handlers
7. **Formatters** → Output formatting
8. **Main** → Entry point and REPL

---

## Complexity Tracking

> No complexity violations. All design decisions follow Constitution principles.

| Decision | Rationale | Simpler Alternative Rejected |
|----------|-----------|------------------------------|
| Layered architecture | Enables Phase 2 reuse | Direct CLI-to-store would require rewrite |
| Custom exceptions | Clear error taxonomy | Generic exceptions would be less descriptive |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| argparse limitations | Low | Medium | Switch to Click in Phase 2 if needed |
| ID collision after delete | Low | Low | IDs never reused in Phase 1 |
| Memory overflow (1000+ todos) | Low | Low | Acceptable for Phase 1 scope |

---

## Next Steps

1. Run `/sp.tasks` to generate implementation task list
2. Begin TDD cycle: Write failing tests first
3. Implement in layer order (Models → Store → Service → CLI)
4. Verify against spec acceptance scenarios
5. Run quality checks (ruff, mypy, pytest)

---

## Artifacts Generated

| Artifact | Path | Status |
|----------|------|--------|
| Specification | `specs/001-console-todo-cli/spec.md` | Complete |
| Research | `specs/001-console-todo-cli/research.md` | Complete |
| Data Model | `specs/001-console-todo-cli/data-model.md` | Complete |
| CLI Contract | `specs/001-console-todo-cli/contracts/cli-contract.md` | Complete |
| Quality Checklist | `specs/001-console-todo-cli/checklists/requirements.md` | Complete |
| Implementation Plan | `specs/001-console-todo-cli/plan.md` | Complete |
| Quickstart | `specs/001-console-todo-cli/quickstart.md` | Pending |
| Tasks | `specs/001-console-todo-cli/tasks.md` | Next Phase |
