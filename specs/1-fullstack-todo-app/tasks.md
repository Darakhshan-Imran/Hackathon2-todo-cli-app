# Tasks: Full-Stack Todo Application

**Input**: Design documents from `/specs/1-fullstack-todo-app/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/openapi.yaml ✅

**Tests**: Tests are MANDATORY per Constitution (Principle XI, XXIII) - TDD with 80% coverage target.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `fullstack-todo-app/backend/`
- **Frontend**: `fullstack-todo-app/frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

### Backend Setup

- [x] T001 [P] Create backend project structure per plan.md in `fullstack-todo-app/backend/`
- [x] T002 [P] Initialize Python project with pyproject.toml, uv dependencies (FastAPI 0.104+, SQLModel, python-jose, passlib[bcrypt], uvicorn, alembic, asyncpg)
- [x] T003 [P] Configure ruff and mypy in pyproject.toml for linting and type checking
- [x] T004 Create app/main.py with FastAPI app instance and lifespan handler
- [x] T005 Create app/config.py with pydantic-settings for environment variables

### Frontend Setup

- [x] T006 [P] Create frontend project structure per plan.md in `fullstack-todo-app/frontend/`
- [x] T007 [P] Initialize Next.js 14 project with TypeScript, Tailwind CSS, ESLint
- [x] T008 [P] Configure tsconfig.json with strict: true, no implicit any
- [x] T009 Create tailwind.config.ts with dark mode class strategy
- [x] T010 Create frontend/types/api.ts with APIResponse and PaginatedData interfaces

### Docker Setup

- [x] T011 [P] Create fullstack-todo-app/docker-compose.yml for local development
- [x] T012 [P] Create backend/.env.example with all required environment variables
- [x] T013 [P] Create frontend/.env.example with NEXT_PUBLIC_API_URL

**Checkpoint**: Project scaffolding complete - both projects can start (with placeholder routes)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Foundation

- [x] T014 Create app/db/engine.py with async SQLAlchemy engine for Neon PostgreSQL
- [x] T015 Create app/db/base.py with SQLModel metadata and async session factory
- [x] T016 Create app/models/enums.py with TodoStatus and Priority enums
- [x] T017 Create app/models/user.py with User SQLModel (id, email, username, password_hash, timestamps, deleted_at)
- [x] T018 Create app/models/todo.py with Todo SQLModel (id, user_id FK, title, description, status, priority, due_date, tags JSONB, timestamps, deleted_at)
- [x] T019 Initialize Alembic in backend/alembic/ with async configuration
- [x] T020 Create initial Alembic migration for users and todos tables with indexes

### Security Foundation

- [x] T021 Create app/security/password.py with bcrypt hash/verify functions (12 rounds)
- [x] T022 Create app/security/jwt.py with create_access_token, create_refresh_token, verify_token functions
- [x] T023 Create app/utils/exceptions.py with custom exception classes (AuthenticationError, AuthorizationError, NotFoundError, ValidationError)
- [x] T024 Create app/middleware/error_handler.py with global exception handlers returning consistent response format

### API Foundation

- [x] T025 Create app/models/schemas.py with all Pydantic request/response schemas per data-model.md
- [x] T026 Create app/dependencies.py with get_db_session dependency
- [x] T027 Create app/api/v1/router.py to combine all v1 routes
- [x] T028 Create app/api/v1/health.py with GET /health endpoint (database connectivity check)
- [x] T029 Create app/utils/logger.py with structured logging configuration
- [x] T030 Add CORS middleware to main.py with configurable origins

### Frontend Foundation

- [x] T031 Create frontend/services/api.ts with Axios instance and base configuration
- [x] T032 Create frontend/types/user.ts with User, UserCreate interfaces
- [x] T033 Create frontend/types/todo.ts with Todo, TodoCreate, TodoUpdate, TodoStatus, Priority types
- [x] T034 Create frontend/lib/validators.ts with Zod schemas for form validation
- [x] T035 Create frontend/components/common/Button.tsx reusable component
- [x] T036 Create frontend/components/common/Input.tsx reusable component
- [x] T037 Create frontend/components/common/LoadingSpinner.tsx component
- [x] T038 Create frontend/components/common/ErrorAlert.tsx component
- [x] T039 Create frontend/components/layout/Header.tsx component
- [x] T040 Create frontend/app/layout.tsx root layout with Tailwind styles

### Foundation Tests

- [x] T041 Create backend/tests/conftest.py with async test fixtures, test database setup
- [x] T042 [P] Create backend/tests/unit/test_security.py for password and JWT functions
- [x] T043 [P] Create backend/tests/integration/test_health.py for health endpoint

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can create accounts, log in securely, refresh tokens, and log out

**Independent Test**: Complete signup, login, token refresh, and logout flows

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T044 [P] [US1] Create backend/tests/unit/test_auth_service.py with tests for register, authenticate, token creation
- [x] T045 [P] [US1] Create backend/tests/integration/test_auth_api.py with tests for /auth/signup, /auth/login, /auth/refresh, /auth/logout

### Implementation for User Story 1

- [x] T046 [US1] Create app/services/auth_service.py with register_user, authenticate_user, create_tokens, verify_refresh_token
- [x] T047 [US1] Create app/services/user_service.py with get_by_email, get_by_username, get_by_id
- [x] T048 [US1] Create app/dependencies.py get_current_user dependency (JWT → User)
- [x] T049 [US1] Create app/api/v1/auth.py with POST /auth/signup endpoint
- [x] T050 [US1] Add POST /auth/login endpoint to auth.py (return access_token, set refresh_token cookie)
- [x] T051 [US1] Add POST /auth/refresh endpoint to auth.py (rotate refresh token)
- [x] T052 [US1] Add POST /auth/logout endpoint to auth.py (clear refresh token cookie)
- [x] T053 [US1] Add validation for email format, username pattern, password requirements in schemas.py
- [x] T054 [US1] Add security event logging for login attempts and failed authentications

### Frontend Implementation for User Story 1

- [x] T055 [P] [US1] Create frontend/services/auth.service.ts with signup, login, logout, refreshToken API calls
- [x] T056 [US1] Create frontend/context/AuthContext.tsx with AuthProvider, useAuth hook
- [x] T057 [US1] Add token refresh interceptor to frontend/services/api.ts
- [x] T058 [US1] Create frontend/lib/auth.ts with token storage utilities (memory only for access token)
- [x] T059 [US1] Create frontend/components/auth/LoginForm.tsx with React Hook Form + Zod validation
- [x] T060 [US1] Create frontend/components/auth/SignupForm.tsx with React Hook Form + Zod validation
- [x] T061 [US1] Create frontend/app/(auth)/login/page.tsx login page
- [x] T062 [US1] Create frontend/app/(auth)/signup/page.tsx signup page
- [x] T063 [US1] Create frontend/components/auth/AuthGuard.tsx for protected route wrapper
- [x] T064 [US1] Add auth state persistence check on app load (try refresh if no access token)

### User Story 1 E2E Test

- [x] T065 [US1] Create frontend E2E test: signup → login → access dashboard → logout flow

**Checkpoint**: User Story 1 complete - users can register, login, and maintain sessions

---

## Phase 4: User Story 2 - Todo CRUD Operations (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create, view, update, and delete their todos

**Independent Test**: Create a todo, view in list, edit, mark complete, delete

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T066 [P] [US2] Create backend/tests/unit/test_todo_service.py with tests for create, get, list, update, soft_delete
- [x] T067 [P] [US2] Create backend/tests/integration/test_todos_api.py with tests for all /todos endpoints
- [x] T068 [P] [US2] Create backend/tests/integration/test_user_isolation.py verifying users cannot access other users' todos

### Implementation for User Story 2

- [x] T069 [US2] Create app/services/todo_service.py with create_todo (requires user_id)
- [x] T070 [US2] Add get_todo method to todo_service.py (filter by user_id, exclude soft-deleted)
- [x] T071 [US2] Add list_todos method to todo_service.py (filter by user_id, exclude soft-deleted)
- [x] T072 [US2] Add update_todo method to todo_service.py (verify ownership, update fields)
- [x] T073 [US2] Add soft_delete_todo method to todo_service.py (set deleted_at timestamp)
- [x] T074 [US2] Create app/api/v1/todos.py with POST /todos endpoint (create with defaults)
- [x] T075 [US2] Add GET /todos endpoint to todos.py (list user's todos)
- [x] T076 [US2] Add GET /todos/{id} endpoint to todos.py (get single todo, 404 if not owned)
- [x] T077 [US2] Add PATCH /todos/{id} endpoint to todos.py (partial update)
- [x] T078 [US2] Add DELETE /todos/{id} endpoint to todos.py (soft delete)
- [x] T079 [US2] Ensure all todo queries include user_id filter in service layer

### Frontend Implementation for User Story 2

- [x] T080 [P] [US2] Create frontend/services/todo.service.ts with createTodo, getTodo, getTodos, updateTodo, deleteTodo API calls
- [x] T081 [US2] Create frontend/hooks/useTodos.ts hook for todo state management
- [x] T082 [US2] Create frontend/components/todos/TodoItem.tsx component (display single todo)
- [x] T083 [US2] Create frontend/components/todos/TodoList.tsx component (render list of TodoItems)
- [x] T084 [US2] Create frontend/components/todos/TodoForm.tsx component (create/edit form with validation)
- [x] T085 [US2] Create frontend/app/(dashboard)/layout.tsx with AuthGuard wrapper
- [x] T086 [US2] Create frontend/app/(dashboard)/todos/page.tsx todo list page
- [x] T087 [US2] Create frontend/app/(dashboard)/todos/new/page.tsx create todo page
- [x] T088 [US2] Create frontend/app/(dashboard)/todos/[id]/page.tsx todo detail/edit page
- [x] T089 [US2] Add status toggle functionality to TodoItem (pending ↔ in_progress ↔ completed)
- [x] T090 [US2] Add delete confirmation and soft delete functionality

### User Story 2 E2E Test

- [x] T091 [US2] Create frontend E2E test: create todo → view in list → edit → mark complete → delete

**Checkpoint**: User Story 2 complete - users can fully manage their todos

---

## Phase 5: User Story 3 - Todo List with Filtering and Pagination (Priority: P2)

**Goal**: Users can filter, sort, and paginate their todo list

**Independent Test**: Create multiple todos, use filters, verify pagination works

### Tests for User Story 3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T092 [P] [US3] Add tests to test_todo_service.py for filtering by status, priority
- [x] T093 [P] [US3] Add tests to test_todos_api.py for pagination, sorting, filtering query params

### Implementation for User Story 3

- [x] T094 [US3] Update todo_service.py list_todos with status filter parameter
- [x] T095 [US3] Update todo_service.py list_todos with priority filter parameter
- [x] T096 [US3] Update todo_service.py list_todos with sort_by and sort_order parameters
- [x] T097 [US3] Update todo_service.py list_todos with pagination (page, per_page) returning total count
- [x] T098 [US3] Update GET /todos endpoint with query params: page, per_page, status, priority, sort_by, sort_order
- [x] T099 [US3] Return paginated response format: {items, page, per_page, total, total_pages}

### Frontend Implementation for User Story 3

- [x] T100 [US3] Create frontend/components/todos/TodoFilters.tsx (status, priority dropdowns)
- [x] T101 [US3] Create frontend/components/todos/TodoPagination.tsx (page navigation)
- [x] T102 [US3] Update useTodos hook with filter and pagination state
- [x] T103 [US3] Update todo list page with filter controls and pagination UI
- [x] T104 [US3] Add sort controls (by created_at, due_date, priority)
- [x] T105 [US3] Add clear filters functionality

### User Story 3 E2E Test

- [x] T106 [US3] Create frontend E2E test: create 25 todos → filter by status → paginate → sort

**Checkpoint**: User Story 3 complete - users can efficiently find and organize todos

---

## Phase 6: User Story 4 - User Profile Management (Priority: P3)

**Goal**: Users can view and update their profile information

**Independent Test**: View profile, update username, verify changes persist

### Tests for User Story 4 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T107 [P] [US4] Create backend/tests/unit/test_user_service.py with tests for get_profile, update_profile
- [x] T108 [P] [US4] Create backend/tests/integration/test_users_api.py with tests for GET/PATCH /users/me

### Implementation for User Story 4

- [x] T109 [US4] Add update_user method to user_service.py (username only, with uniqueness check)
- [x] T110 [US4] Create app/api/v1/users.py with GET /users/me endpoint
- [x] T111 [US4] Add PATCH /users/me endpoint to users.py (update username)
- [x] T112 [US4] Add conflict handling for duplicate username (409 response)

### Frontend Implementation for User Story 4

- [x] T113 [US4] Create frontend/services/user.service.ts with getProfile, updateProfile API calls
- [x] T114 [US4] Create frontend/components/profile/ProfileForm.tsx with username edit
- [x] T115 [US4] Create frontend/app/(dashboard)/profile/page.tsx profile page
- [x] T116 [US4] Add success toast on profile update
- [x] T117 [US4] Handle username conflict error in UI

### User Story 4 E2E Test

- [x] T118 [US4] Create frontend E2E test: view profile → update username → verify change

**Checkpoint**: User Story 4 complete - users can manage their profile

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Production readiness, optimization, and documentation

### Code Quality

- [ ] T119 [P] Run ruff check and fix all linting issues in backend
- [ ] T120 [P] Run mypy and fix all type errors in backend
- [ ] T121 [P] Run ESLint and fix all issues in frontend
- [ ] T122 [P] Run TypeScript type check and fix all errors in frontend
- [ ] T123 Verify 80% test coverage for backend (pytest --cov)
- [ ] T124 Verify frontend component test coverage

### Security Hardening

- [ ] T125 [P] Add rate limiting to auth endpoints (10 req/min per IP)
- [ ] T126 [P] Add rate limiting to general API (100 req/min per user)
- [ ] T127 Verify no secrets in code or logs (audit codebase)
- [ ] T128 Verify all inputs are validated (review all endpoints)
- [x] T129 Add security headers middleware (X-Content-Type-Options, X-Frame-Options)

### Performance Optimization

- [x] T130 [P] Add database indexes for common queries (verify indexes from data-model.md exist)
- [ ] T131 [P] Optimize frontend bundle (verify dynamic imports, code splitting)
- [ ] T132 Test API response times with 1000 todos (must be <2s)

### Documentation

- [x] T133 [P] Create backend/README.md with setup and API documentation
- [x] T134 [P] Create frontend/README.md with setup and development guide
- [x] T135 [P] Create fullstack-todo-app/README.md project overview
- [ ] T136 Validate quickstart.md instructions work end-to-end

### Deployment

- [x] T137 Create backend/Dockerfile with multi-stage build
- [x] T138 Create frontend/Dockerfile for production build
- [x] T139 Update docker-compose.yml with production configuration
- [x] T140 Create .github/workflows/ci.yml for automated testing (optional)

### Final Validation

- [ ] T141 Run all backend tests (pytest -v)
- [ ] T142 Run all frontend tests (npm test)
- [ ] T143 Run E2E tests (npm run test:e2e)
- [ ] T144 Complete security checklist from plan.md
- [ ] T145 Verify all 30 functional requirements from spec.md are implemented

**Checkpoint**: Application production-ready

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (Auth) should complete before US2 (requires authentication)
  - US2 (Todo CRUD) should complete before US3 (requires todos to exist)
  - US4 (Profile) can run in parallel with US3 after US1 completes
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) ←── BLOCKS ALL
    ↓
Phase 3 (US1: Auth) ←── P1 MVP
    ↓
Phase 4 (US2: Todo CRUD) ←── P1 MVP (requires auth)
    ↓
┌───────────────────────────────┐
│                               │
Phase 5 (US3: Filtering)    Phase 6 (US4: Profile)
    P2                          P3
│                               │
└───────────────────────────────┘
    ↓
Phase 7 (Polish)
```

### Within Each User Story

1. Tests MUST be written and FAIL before implementation
2. Backend services before API endpoints
3. API endpoints before frontend services
4. Frontend services before UI components
5. UI components before pages
6. E2E tests after all story components complete

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Backend and Frontend foundation can run in parallel
- Tests for a user story marked [P] can run in parallel
- US3 and US4 can run in parallel (after US1 completes)
- All Polish tasks marked [P] can run in parallel

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Auth)
4. Complete Phase 4: User Story 2 (Todo CRUD)
5. **STOP and VALIDATE**: Test complete auth + todo flow
6. Deploy MVP if ready

### Full Feature Set

1. Setup + Foundational → Foundation ready
2. Add User Story 1 (Auth) → Test independently
3. Add User Story 2 (Todo CRUD) → Test independently → **MVP Complete!**
4. Add User Story 3 (Filtering/Pagination) → Test independently
5. Add User Story 4 (Profile) → Test independently
6. Polish → Production ready

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD per Constitution)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- User isolation is CRITICAL - verify with test_user_isolation.py

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1 | T001-T013 | Setup (13 tasks) |
| Phase 2 | T014-T043 | Foundational (30 tasks) |
| Phase 3 | T044-T065 | US1: Authentication (22 tasks) |
| Phase 4 | T066-T091 | US2: Todo CRUD (26 tasks) |
| Phase 5 | T092-T106 | US3: Filtering/Pagination (15 tasks) |
| Phase 6 | T107-T118 | US4: Profile (12 tasks) |
| Phase 7 | T119-T145 | Polish (27 tasks) |
| **Total** | **145 tasks** | |

---

## Related Documents

- [Specification](./spec.md) - Feature requirements (30 FRs, 4 user stories)
- [Implementation Plan](./plan.md) - Architecture and sprint breakdown
- [Data Model](./data-model.md) - Entity definitions and schemas
- [API Contracts](./contracts/openapi.yaml) - OpenAPI specification (12 endpoints)
- [Quickstart](./quickstart.md) - Developer setup guide
- [Constitution](../../.specify/memory/constitution.md) - Governance rules
