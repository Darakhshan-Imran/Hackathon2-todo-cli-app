# Tasks: Phase 1 Console Todo CLI

**Input**: Design documents from `specs/001-console-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Tests are included per Constitution XI (Test-First Development) - TDD is mandatory.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Reusability Legend

- **[REUSE]**: Component reusable in Phase 2+ (cloud-native ready)
- **[P1-ONLY]**: Phase 1 specific, will be replaced in future phases

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize project structure and configure development environment

- [ ] T001 Create project directory structure per plan.md in src/
- [ ] T002 [P] Create src/__init__.py with package metadata
- [ ] T003 [P] Create src/models/__init__.py
- [ ] T004 [P] Create src/store/__init__.py
- [ ] T005 [P] Create src/services/__init__.py
- [ ] T006 [P] Create src/cli/__init__.py
- [ ] T007 [P] Create src/exceptions/__init__.py
- [ ] T008 [P] Create src/utils/__init__.py
- [ ] T009 Update pyproject.toml with dev dependencies (pytest, ruff, mypy)
- [ ] T010 [P] Create tests/__init__.py
- [ ] T011 [P] Create tests/unit/__init__.py
- [ ] T012 [P] Create tests/integration/__init__.py
- [ ] T013 Create tests/conftest.py with shared fixtures

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Models [REUSE]

- [ ] T014 [P] Create TodoStatus enum in src/models/status.py
- [ ] T015 [P] Create Todo dataclass in src/models/todo.py
- [ ] T016 Update src/models/__init__.py to export Todo and TodoStatus

### Exceptions [REUSE]

- [ ] T017 [P] Create custom exceptions in src/exceptions/errors.py (TodoError, TodoNotFoundError, ValidationError)
- [ ] T018 Update src/exceptions/__init__.py to export all exceptions

### Validators [REUSE]

- [ ] T019 Create input validators in src/utils/validators.py (validate_title, validate_id)
- [ ] T020 Update src/utils/__init__.py to export validators

### Store [P1-ONLY]

- [ ] T021 Create TodoStore class in src/store/todo_store.py with in-memory dict storage
- [ ] T022 Update src/store/__init__.py to export TodoStore

### Service [REUSE]

- [ ] T023 Create TodoService class in src/services/todo_service.py with CRUD methods
- [ ] T024 Update src/services/__init__.py to export TodoService

### Foundational Tests (TDD - Write First, Must Fail)

- [ ] T025 [P] Write tests for TodoStatus enum in tests/unit/test_models.py
- [ ] T026 [P] Write tests for Todo dataclass in tests/unit/test_models.py
- [ ] T027 [P] Write tests for validators in tests/unit/test_validators.py
- [ ] T028 [P] Write tests for exceptions in tests/unit/test_models.py
- [ ] T029 Write tests for TodoStore in tests/unit/test_store.py
- [ ] T030 Write tests for TodoService in tests/unit/test_service.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 & 2 - Add Todo & View Todos (Priority: P1)

**Goal**: Enable users to add todos and view them - the core MVP functionality

**Independent Test**: Run `add "Test"` then `list` to verify todos are created and displayed

### Tests for US1 & US2 (TDD - Write First, Must Fail)

- [ ] T031 [P] [US1] Write CLI tests for add command in tests/integration/test_cli.py
- [ ] T032 [P] [US2] Write CLI tests for list command in tests/integration/test_cli.py

### CLI Infrastructure [P1-ONLY]

- [ ] T033 Create argument parser with subcommands in src/cli/parser.py
- [ ] T034 [P] Create output formatters in src/cli/formatters.py (human + JSON) [REUSE: JSON formatter]
- [ ] T035 Create command handlers base in src/cli/commands.py

### Implementation for US1 - Add Todo

- [ ] T036 [US1] Implement add command handler in src/cli/commands.py
- [ ] T037 [US1] Add add subparser to src/cli/parser.py
- [ ] T038 [US1] Add success/error formatting for add command in src/cli/formatters.py

### Implementation for US2 - View Todos

- [ ] T039 [US2] Implement list command handler in src/cli/commands.py
- [ ] T040 [US2] Add list subparser with --status flag in src/cli/parser.py
- [ ] T041 [US2] Add table formatter for list output in src/cli/formatters.py

### Main Entry Point

- [ ] T042 Create main.py with REPL loop in src/main.py
- [ ] T043 Add welcome message and help hint per FR-023
- [ ] T044 Add help command handler in src/cli/commands.py

**Checkpoint**: MVP complete - users can add and view todos

---

## Phase 4: User Story 3 - Mark Complete/Incomplete (Priority: P2)

**Goal**: Enable users to mark todos as complete or incomplete

**Independent Test**: Run `add "Test"`, `complete 1`, `list` to verify status changes

### Tests for US3 (TDD - Write First, Must Fail)

- [ ] T045 [P] [US3] Write CLI tests for complete command in tests/integration/test_cli.py
- [ ] T046 [P] [US3] Write CLI tests for incomplete command in tests/integration/test_cli.py

### Implementation for US3

- [ ] T047 [US3] Implement complete command handler in src/cli/commands.py
- [ ] T048 [US3] Implement incomplete command handler in src/cli/commands.py
- [ ] T049 [US3] Add complete/incomplete subparsers in src/cli/parser.py
- [ ] T050 [US3] Add success/error formatting for status commands in src/cli/formatters.py

**Checkpoint**: Status management complete - users can track completion

---

## Phase 5: User Story 4 - Update Todo (Priority: P2)

**Goal**: Enable users to update todo title and/or description

**Independent Test**: Run `add "Old"`, `update 1 --title "New"`, `show 1` to verify update

### Tests for US4 (TDD - Write First, Must Fail)

- [ ] T051 [P] [US4] Write CLI tests for update command in tests/integration/test_cli.py

### Implementation for US4

- [ ] T052 [US4] Implement update command handler in src/cli/commands.py
- [ ] T053 [US4] Add update subparser with --title and --description flags in src/cli/parser.py
- [ ] T054 [US4] Add validation for at least one field required in update handler

**Checkpoint**: Update functionality complete

---

## Phase 6: User Story 5 - Delete Todo (Priority: P3)

**Goal**: Enable users to delete todos

**Independent Test**: Run `add "Test"`, `delete 1`, `list` to verify deletion

### Tests for US5 (TDD - Write First, Must Fail)

- [ ] T055 [P] [US5] Write CLI tests for delete command in tests/integration/test_cli.py

### Implementation for US5

- [ ] T056 [US5] Implement delete command handler in src/cli/commands.py
- [ ] T057 [US5] Add delete subparser in src/cli/parser.py

**Checkpoint**: Delete functionality complete

---

## Phase 7: User Story 6 - Show Todo Details (Priority: P3)

**Goal**: Enable users to view full details of a single todo

**Independent Test**: Run `add "Test" "Long description"`, `show 1` to see full details

### Tests for US6 (TDD - Write First, Must Fail)

- [ ] T058 [P] [US6] Write CLI tests for show command in tests/integration/test_cli.py

### Implementation for US6

- [ ] T059 [US6] Implement show command handler in src/cli/commands.py
- [ ] T060 [US6] Add show subparser in src/cli/parser.py
- [ ] T061 [US6] Add detail formatter for single todo in src/cli/formatters.py

**Checkpoint**: All user stories complete

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Finalize quality, edge cases, and observability

### Edge Cases & Error Handling

- [ ] T062 [P] Add empty input handling (show help) in src/main.py
- [ ] T063 [P] Add unknown command handling in src/cli/commands.py
- [ ] T064 [P] Add exit/quit command handlers in src/cli/commands.py
- [ ] T065 Add --json global flag support across all commands

### Quality Assurance

- [ ] T066 Run ruff linter and fix all issues
- [ ] T067 Run mypy type checker and fix all issues
- [ ] T068 Run pytest with coverage and verify 80%+ coverage
- [ ] T069 Validate all commands against cli-contract.md
- [ ] T070 Run quickstart.md scenarios manually to verify

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (BLOCKS all user stories)
    ↓
Phase 3: US1 & US2 (P1) - Add & List → MVP
    ↓
Phase 4: US3 (P2) - Complete/Incomplete
    ↓
Phase 5: US4 (P2) - Update
    ↓
Phase 6: US5 (P3) - Delete
    ↓
Phase 7: US6 (P3) - Show
    ↓
Phase 8: Polish
```

### User Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|------------|-------------------|
| US1 (Add) | Foundational | US2 |
| US2 (List) | Foundational | US1 |
| US3 (Complete) | US1 + US2 | US4 |
| US4 (Update) | US1 + US2 | US3 |
| US5 (Delete) | US1 + US2 | US6 |
| US6 (Show) | US1 + US2 | US5 |

### Within Each User Story

1. Tests MUST be written first and FAIL before implementation (TDD)
2. Models before services
3. Services before CLI handlers
4. CLI handlers before formatters
5. Integration test must pass before story is complete

---

## Parallel Execution Examples

### Phase 2 - Foundational (Max Parallelism)

```bash
# Run all model/exception tasks in parallel:
T014: Create TodoStatus enum
T015: Create Todo dataclass
T017: Create custom exceptions
T019: Create validators
# Then sequentially:
T021: Create TodoStore (needs models)
T023: Create TodoService (needs store)
```

### Phase 3 - US1 & US2 (Parallel Stories)

```bash
# Tests first (parallel):
T031: CLI tests for add
T032: CLI tests for list
# Then infrastructure:
T033: Argument parser
T034: Output formatters
# Then story-specific (can parallel US1/US2):
T036-T038: Add command (US1)
T039-T041: List command (US2)
```

---

## Implementation Strategy

### TDD Cycle (Per Task)

1. Write test → Run test → Verify FAIL (red)
2. Write minimal code to pass → Run test → Verify PASS (green)
3. Refactor if needed → Run test → Verify still PASS
4. Commit

### MVP First (Recommended Path)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 & US2 (Add + List)
4. **STOP and VALIDATE**: Test MVP independently
5. Demo/deploy if satisfactory
6. Continue with remaining stories

### Incremental Delivery

| Increment | Stories | Value Delivered |
|-----------|---------|-----------------|
| MVP | US1 + US2 | Create and view todos |
| +Status | US3 | Track completion |
| +Edit | US4 | Modify todos |
| +Delete | US5 | Remove todos |
| +Details | US6 | View full info |

---

## Cloud-Native Blueprint Mapping

| Task Component | Reusable? | Phase 2+ Mapping |
|----------------|-----------|------------------|
| Todo dataclass | [REUSE] | ORM model |
| TodoStatus enum | [REUSE] | Same enum |
| Validators | [REUSE] | Same validators |
| TodoService | [REUSE] | API controller logic |
| Exceptions | [REUSE] | HTTP error responses |
| TodoStore | [P1-ONLY] | Repository pattern |
| CLI parser | [P1-ONLY] | Not needed |
| Formatters (JSON) | [REUSE] | API response format |

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 70 |
| Setup Phase | 13 |
| Foundational Phase | 17 |
| US1 & US2 (P1) | 14 |
| US3 (P2) | 6 |
| US4 (P2) | 4 |
| US5 (P3) | 3 |
| US6 (P3) | 4 |
| Polish Phase | 9 |
| Parallelizable Tasks | 28 |
| Reusable Components | 60% |

---

## Notes

- [P] tasks = different files, no dependencies
- [US#] label maps task to specific user story for traceability
- TDD is mandatory per Constitution XI
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
