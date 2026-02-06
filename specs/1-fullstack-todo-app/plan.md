# Implementation Plan: Full-Stack Todo Application

**Branch**: `1-fullstack-todo-app` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-fullstack-todo-app/spec.md`

## Summary

Build a production-ready fullstack todo application extending the Phase 1 CLI with:
- **Backend**: FastAPI REST API with JWT authentication, SQLModel ORM, Neon PostgreSQL
- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, and secure token management
- **Core Features**: User registration/login, todo CRUD with user isolation, filtering, pagination

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**:
- Backend: FastAPI 0.104+, SQLModel, python-jose, passlib[bcrypt], uvicorn
- Frontend: Next.js 14+, Axios, React Hook Form, Zod

**Storage**: Neon PostgreSQL (serverless) with SQLModel ORM
**Testing**: pytest + pytest-asyncio (backend), Jest + RTL + Playwright (frontend)
**Target Platform**: Linux server (backend), Web browsers (frontend)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: <2s response time for 1000 todos, 100 concurrent users
**Constraints**: JWT access tokens ≤15min, refresh tokens ≤7 days, bcrypt ≥12 rounds
**Scale/Scope**: Single-tenant, ~1000 users, ~10k todos per user

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec-Driven Development | ✅ PASS | spec.md created with 30 FRs, 4 user stories |
| IV. Python Standards | ✅ PASS | Python 3.13+, uv package manager, pyproject.toml |
| V. Clean Code Architecture | ✅ PASS | Modular structure: api/, services/, models/ |
| IX. Modular Extensibility | ✅ PASS | Service layer separation, dependency injection |
| X. Security-First | ✅ PASS | JWT auth, bcrypt 12+, CORS, input validation |
| XI. Test-First Development | ✅ PASS | TDD with pytest, 80% coverage target |
| XII. Observability | ✅ PASS | Structured logging, health check endpoint |
| XIII. Simplicity (YAGNI) | ✅ PASS | Minimal viable features, no over-engineering |
| XIV. JWT Token Strategy | ✅ PASS | Access 15min, refresh 7d, HttpOnly cookies |
| XV. User Data Isolation | ✅ PASS | Service-layer user_id filtering, 404 on cross-access |
| XVI. Security Standards | ✅ PASS | bcrypt 12+, CORS explicit origins, rate limiting |
| XVII. FastAPI Architecture | ✅ PASS | Async operations, dependency injection, Pydantic |
| XVIII. Database Standards | ✅ PASS | SQLModel, Alembic migrations, proper indexes |
| XIX. Frontend Auth Flow | ✅ PASS | Memory tokens, HttpOnly refresh, auto-refresh |
| XX. UI/UX Standards | ✅ PASS | Tailwind, responsive, WCAG 2.1 AA, dark mode |
| XXI. API Contract Standards | ✅ PASS | REST conventions, consistent response format |
| XXIII. Testing Principles | ✅ PASS | Unit, integration, E2E coverage planned |
| XXIV. Environment Config | ✅ PASS | .env files, environment variables documented |
| XXV. Deployment Readiness | ✅ PASS | Dockerfile, health checks, Docker Compose |
| XXVI. Migration Path | ✅ PASS | CLI preserved in cli-todo-app/, domain logic reused |
| XXVII. TypeScript Standards | ✅ PASS | strict: true, no any, Zod validation |

**Gate Status**: ✅ ALL PASSED - Proceed to implementation

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SYSTEM ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                           FRONTEND (Next.js 14)                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │ │
│  │  │  Auth Pages  │  │ Todo Pages   │  │  Components  │  │   Hooks     │  │ │
│  │  │  - Login     │  │  - List      │  │  - TodoItem  │  │  - useAuth  │  │ │
│  │  │  - Signup    │  │  - Detail    │  │  - TodoForm  │  │  - useTodos │  │ │
│  │  └──────┬───────┘  └──────┬───────┘  │  - Layout    │  │  - useAxios │  │ │
│  │         │                 │          └──────────────┘  └─────────────┘  │ │
│  │         └────────┬────────┘                                              │ │
│  │                  ▼                                                       │ │
│  │         ┌──────────────────┐                                             │ │
│  │         │   API Service    │  ← Axios + JWT Interceptor                  │ │
│  │         │  (auth, todos)   │                                             │ │
│  │         └────────┬─────────┘                                             │ │
│  └──────────────────┼───────────────────────────────────────────────────────┘ │
│                     │ HTTPS                                                   │
│                     ▼                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                          BACKEND (FastAPI)                               │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐   │ │
│  │  │                        API Layer (/api/v1)                        │   │ │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │   │ │
│  │  │  │  auth.py    │  │  todos.py   │  │  users.py   │  │ health.py│ │   │ │
│  │  │  │  - signup   │  │  - list     │  │  - me       │  │  - check │ │   │ │
│  │  │  │  - login    │  │  - create   │  │  - update   │  └──────────┘ │   │ │
│  │  │  │  - refresh  │  │  - read     │  └─────────────┘               │   │ │
│  │  │  │  - logout   │  │  - update   │                                │   │ │
│  │  │  └──────┬──────┘  │  - delete   │                                │   │ │
│  │  │         │         └──────┬──────┘                                │   │ │
│  │  └─────────┼────────────────┼───────────────────────────────────────┘   │ │
│  │            │                │                                            │ │
│  │            ▼                ▼                                            │ │
│  │  ┌────────────────────────────────────────────────────────────────┐     │ │
│  │  │                      Dependencies Layer                         │     │ │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │     │ │
│  │  │  │ get_current_user│  │   get_db_session │  │   get_config   │  │     │ │
│  │  │  │  (JWT → User)   │  │  (async session) │  │  (settings)    │  │     │ │
│  │  │  └─────────────────┘  └─────────────────┘  └────────────────┘  │     │ │
│  │  └────────────────────────────────────────────────────────────────┘     │ │
│  │            │                │                                            │ │
│  │            ▼                ▼                                            │ │
│  │  ┌────────────────────────────────────────────────────────────────┐     │ │
│  │  │                       Service Layer                             │     │ │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │     │ │
│  │  │  │  AuthService    │  │   TodoService   │  │   UserService  │  │     │ │
│  │  │  │  - register     │  │  - create       │  │  - get_by_id   │  │     │ │
│  │  │  │  - authenticate │  │  - get (w/user) │  │  - update      │  │     │ │
│  │  │  │  - create_tokens│  │  - list (filter)│  │                │  │     │ │
│  │  │  │  - verify_token │  │  - update       │  └────────────────┘  │     │ │
│  │  │  └─────────────────┘  │  - soft_delete  │                      │     │ │
│  │  │                       └─────────────────┘                      │     │ │
│  │  │        ↑ User isolation: ALL queries include user_id filter    │     │ │
│  │  └────────────────────────────────────────────────────────────────┘     │ │
│  │                           │                                              │ │
│  │                           ▼                                              │ │
│  │  ┌────────────────────────────────────────────────────────────────┐     │ │
│  │  │                       Model Layer (SQLModel)                    │     │ │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │     │ │
│  │  │  │     User        │  │      Todo       │  │     Enums      │  │     │ │
│  │  │  │  - id (UUID)    │  │  - id (UUID)    │  │  - TodoStatus  │  │     │ │
│  │  │  │  - email        │  │  - user_id (FK) │  │  - Priority    │  │     │ │
│  │  │  │  - username     │  │  - title        │  │                │  │     │ │
│  │  │  │  - password_hash│  │  - status       │  └────────────────┘  │     │ │
│  │  │  │  - timestamps   │  │  - priority     │                      │     │ │
│  │  │  │  - deleted_at   │  │  - timestamps   │                      │     │ │
│  │  │  └─────────────────┘  │  - deleted_at   │                      │     │ │
│  │  │                       └─────────────────┘                      │     │ │
│  │  └────────────────────────────────────────────────────────────────┘     │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                          │
│                                    ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │                        DATABASE (Neon PostgreSQL)                         │ │
│  │  ┌──────────────────────────────────────────────────────────────────────┐│ │
│  │  │  users                              │  todos                          ││ │
│  │  │  ─────                              │  ─────                          ││ │
│  │  │  id UUID PK                         │  id UUID PK                     ││ │
│  │  │  email VARCHAR(255) UNIQUE INDEX    │  user_id UUID FK → users.id     ││ │
│  │  │  username VARCHAR(30) UNIQUE INDEX  │  title VARCHAR(255) NOT NULL    ││ │
│  │  │  password_hash VARCHAR              │  description TEXT               ││ │
│  │  │  created_at TIMESTAMPTZ            │  status ENUM                    ││ │
│  │  │  updated_at TIMESTAMPTZ            │  priority ENUM                  ││ │
│  │  │  deleted_at TIMESTAMPTZ            │  due_date TIMESTAMPTZ           ││ │
│  │  │                                     │  tags JSONB                     ││ │
│  │  │                                     │  created_at TIMESTAMPTZ         ││ │
│  │  │                                     │  updated_at TIMESTAMPTZ         ││ │
│  │  │                                     │  deleted_at TIMESTAMPTZ         ││ │
│  │  │                                     │  INDEX (user_id)                ││ │
│  │  │                                     │  INDEX (user_id, status)        ││ │
│  │  └──────────────────────────────────────────────────────────────────────┘│ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## JWT Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AUTHENTICATION FLOWS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  SIGNUP FLOW                                                                  │
│  ──────────                                                                   │
│  ┌──────────┐    POST /auth/signup     ┌──────────┐    Create User    ┌────┐ │
│  │  Client  │ ──────────────────────►  │  Backend │ ───────────────► │ DB │ │
│  │          │    {email, username,     │          │    hash password  │    │ │
│  │          │     password}            │          │    with bcrypt    │    │ │
│  │          │                          │          │                   │    │ │
│  │          │  ◄──────────────────────  │          │ ◄───────────────  │    │ │
│  │          │    {access_token}        │          │    user created   │    │ │
│  │          │    + Set-Cookie:         │          │                   │    │ │
│  │          │    refresh_token         │          │                   └────┘ │
│  └──────────┘    (HttpOnly)            └──────────┘                          │
│                                                                               │
│  LOGIN FLOW                                                                   │
│  ──────────                                                                   │
│  ┌──────────┐    POST /auth/login      ┌──────────┐    Verify User    ┌────┐ │
│  │  Client  │ ──────────────────────►  │  Backend │ ───────────────► │ DB │ │
│  │          │    {email, password}     │          │    compare hash   │    │ │
│  │          │                          │          │                   │    │ │
│  │          │  ◄──────────────────────  │          │ ◄───────────────  │    │ │
│  │          │    {access_token}        │          │    user valid     │    │ │
│  │          │    + Set-Cookie:         │          │                   │    │ │
│  │          │    refresh_token         │          │                   └────┘ │
│  └──────────┘    (HttpOnly, 7 days)    └──────────┘                          │
│                                                                               │
│  AUTHENTICATED REQUEST FLOW                                                   │
│  ──────────────────────────                                                   │
│  ┌──────────┐    GET /todos            ┌──────────┐    Query w/      ┌────┐  │
│  │  Client  │ ──────────────────────►  │  Backend │    user_id ────► │ DB │  │
│  │          │    Authorization:        │          │                  │    │  │
│  │          │    Bearer <access>       │          │                  │    │  │
│  │          │                          │ Validate │                  │    │  │
│  │          │  ◄──────────────────────  │   JWT    │ ◄────────────── │    │  │
│  │          │    {success, data}       │ Extract  │    user's todos  │    │  │
│  └──────────┘                          │ user_id  │                  └────┘  │
│                                        └──────────┘                          │
│                                                                               │
│  TOKEN REFRESH FLOW                                                           │
│  ─────────────────                                                            │
│  ┌──────────┐    POST /auth/refresh    ┌──────────┐                          │
│  │  Client  │ ──────────────────────►  │  Backend │                          │
│  │          │    Cookie:               │          │                          │
│  │          │    refresh_token         │ Validate │                          │
│  │          │                          │ refresh  │                          │
│  │          │  ◄──────────────────────  │  token   │                          │
│  │          │    {access_token}        │ Generate │                          │
│  │          │    + Set-Cookie:         │ new pair │                          │
│  └──────────┘    new refresh_token     └──────────┘                          │
│                  (rotation)                                                   │
│                                                                               │
│  TOKEN STRUCTURE                                                              │
│  ───────────────                                                              │
│  Access Token (15 min):                Refresh Token (7 days):               │
│  {                                     {                                     │
│    "sub": "<user_id>",                   "sub": "<user_id>",                 │
│    "type": "access",                     "type": "refresh",                  │
│    "exp": <15min_from_now>,              "jti": "<unique_id>",               │
│    "iat": <issued_at>                    "exp": <7days_from_now>,            │
│  }                                       "iat": <issued_at>                  │
│                                        }                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

### Documentation (this feature)

```text
specs/1-fullstack-todo-app/
├── spec.md              # Feature specification
├── plan.md              # This implementation plan
├── research.md          # Phase 0 research findings
├── data-model.md        # Entity definitions and relationships
├── quickstart.md        # Developer setup guide
├── contracts/           # API contracts (OpenAPI)
│   └── openapi.yaml     # Full API specification
├── checklists/          # Quality checklists
│   └── requirements.md  # Spec validation checklist
└── tasks.md             # Sprint tasks (/sp.tasks output)
```

### Source Code (repository root)

```text
fullstack-todo-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app, lifespan, routers
│   │   ├── config.py                  # Settings from environment
│   │   ├── dependencies.py            # get_db, get_current_user
│   │   ├── constants.py               # App constants
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py          # Combines all v1 routes
│   │   │   │   ├── auth.py            # /auth/* endpoints
│   │   │   │   ├── todos.py           # /todos/* endpoints
│   │   │   │   ├── users.py           # /users/* endpoints
│   │   │   │   └── health.py          # /health endpoint
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py        # Registration, login, tokens
│   │   │   ├── todo_service.py        # Todo CRUD with user isolation
│   │   │   └── user_service.py        # User profile operations
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py                # User SQLModel
│   │   │   ├── todo.py                # Todo SQLModel
│   │   │   ├── enums.py               # TodoStatus, Priority enums
│   │   │   └── schemas.py             # Request/Response Pydantic models
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py              # Async engine, session factory
│   │   │   └── base.py                # SQLModel base, table creation
│   │   ├── security/
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py                 # Token create/verify functions
│   │   │   └── password.py            # Bcrypt hash/verify functions
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   └── error_handler.py       # Global exception handlers
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── validators.py          # Input validation helpers
│   │       ├── exceptions.py          # Custom exception classes
│   │       └── logger.py              # Structured logging setup
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py                # Fixtures, test DB setup
│   │   ├── unit/
│   │   │   ├── __init__.py
│   │   │   ├── test_auth_service.py
│   │   │   ├── test_todo_service.py
│   │   │   ├── test_user_service.py
│   │   │   └── test_security.py
│   │   └── integration/
│   │       ├── __init__.py
│   │       ├── test_auth_api.py
│   │       ├── test_todos_api.py
│   │       ├── test_users_api.py
│   │       └── test_user_isolation.py
│   ├── alembic/
│   │   ├── env.py
│   │   ├── versions/
│   │   └── alembic.ini
│   ├── pyproject.toml
│   ├── .env.example
│   ├── Dockerfile
│   └── README.md
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx                 # Root layout with AuthProvider
│   │   ├── page.tsx                   # Landing/redirect page
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   │   └── page.tsx           # Login page
│   │   │   └── signup/
│   │   │       └── page.tsx           # Signup page
│   │   └── (dashboard)/
│   │       ├── layout.tsx             # Dashboard layout with auth guard
│   │       ├── todos/
│   │       │   ├── page.tsx           # Todo list page
│   │       │   ├── [id]/
│   │       │   │   └── page.tsx       # Todo detail page
│   │       │   └── new/
│   │       │       └── page.tsx       # Create todo page
│   │       └── profile/
│   │           └── page.tsx           # User profile page
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── SignupForm.tsx
│   │   │   └── AuthGuard.tsx
│   │   ├── todos/
│   │   │   ├── TodoList.tsx
│   │   │   ├── TodoItem.tsx
│   │   │   ├── TodoForm.tsx
│   │   │   ├── TodoFilters.tsx
│   │   │   └── TodoPagination.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   └── common/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       ├── LoadingSpinner.tsx
│   │       ├── ErrorAlert.tsx
│   │       └── Toast.tsx
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useTodos.ts
│   │   └── useAxios.ts
│   ├── services/
│   │   ├── api.ts                     # Axios instance with interceptors
│   │   ├── auth.service.ts            # Auth API calls
│   │   └── todo.service.ts            # Todo API calls
│   ├── lib/
│   │   ├── auth.ts                    # Token utilities
│   │   ├── validators.ts              # Zod schemas
│   │   └── utils.ts                   # Helper functions
│   ├── types/
│   │   ├── user.ts                    # User types
│   │   ├── todo.ts                    # Todo types
│   │   └── api.ts                     # API response types
│   ├── context/
│   │   └── AuthContext.tsx            # Auth state provider
│   ├── public/
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── package.json
│   ├── .env.example
│   └── README.md
│
├── docker-compose.yml                  # Local development setup
└── README.md                           # Project overview
```

**Structure Decision**: Web application with separate backend (FastAPI) and frontend (Next.js) directories. Each has its own package management, tests, and deployment configuration.

---

## Development Sprints

### Sprint 1: Backend Foundation

**Goal**: Set up FastAPI project with database connection and models

| Task | Description | Deliverables |
|------|-------------|--------------|
| 1.1 | FastAPI project setup | main.py, config.py, pyproject.toml |
| 1.2 | Database connection | engine.py, async sessions, health check |
| 1.3 | Data models | User, Todo SQLModel classes, enums |
| 1.4 | Create tables | Alembic setup, initial migration |
| 1.5 | Validation | ruff, mypy pass, basic tests |

### Sprint 2: Authentication Implementation

**Goal**: Complete JWT authentication system

| Task | Description | Deliverables |
|------|-------------|--------------|
| 2.1 | Security services | jwt.py, password.py (bcrypt) |
| 2.2 | User service | CRUD, password hashing |
| 2.3 | Auth routes | signup, login, refresh, logout |
| 2.4 | Auth dependencies | get_current_user, token validation |

### Sprint 3: Frontend Setup

**Goal**: Initialize Next.js with API client and layout

| Task | Description | Deliverables |
|------|-------------|--------------|
| 3.1 | Next.js initialization | TypeScript, Tailwind, structure |
| 3.2 | API client | Axios instance, interceptors |
| 3.3 | Layout components | Header, Footer, common UI |

### Sprint 4: Frontend Authentication

**Goal**: Complete frontend auth flow

| Task | Description | Deliverables |
|------|-------------|--------------|
| 4.1 | Auth context | AuthProvider, useAuth hook |
| 4.2 | Auth pages | Login, Signup forms with validation |
| 4.3 | Protected routes | AuthGuard, redirects |

### Sprint 5: Backend Todo API

**Goal**: Complete todo CRUD with user isolation

| Task | Description | Deliverables |
|------|-------------|--------------|
| 5.1 | Todo service | CRUD with user_id filtering |
| 5.2 | Read routes | GET list (paginated), GET by ID |
| 5.3 | Write routes | POST, PATCH, DELETE (soft) |
| 5.4 | Response formatting | Consistent format, error handling |
| 5.5 | Test coverage | Unit + integration tests |

### Sprint 6: Frontend Todos

**Goal**: Complete todo UI with filtering

| Task | Description | Deliverables |
|------|-------------|--------------|
| 6.1 | Todo list page | Display, loading, pagination |
| 6.2 | Filters and sorting | Status, priority, sort controls |
| 6.3 | Create/edit forms | TodoForm component |
| 6.4 | Todo actions | Delete, status toggle |
| 6.5 | Integration testing | E2E tests, accessibility |

### Sprint 7: Integration & Deployment

**Goal**: Production-ready deployment

| Task | Description | Deliverables |
|------|-------------|--------------|
| 7.1 | E2E testing | Complete user journeys |
| 7.2 | Optimization | DB queries, frontend bundle |
| 7.3 | Documentation | READMEs, API docs, diagrams |
| 7.4 | Deployment | Dockerfiles, docker-compose |

---

## Environment Configuration

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname

# JWT Configuration
JWT_SECRET_KEY=your-256-bit-secret-key-here-minimum-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000,https://your-frontend.com

# Environment
ENVIRONMENT=development

# Logging
LOG_LEVEL=INFO
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=Todo App
NEXT_PUBLIC_ENVIRONMENT=development
```

---

## Testing Strategy

### Backend Testing

| Type | Coverage | Tools |
|------|----------|-------|
| Unit | Services, validators | pytest, pytest-asyncio |
| Integration | API endpoints | httpx, test database |
| User Isolation | Cross-user access attempts | Dedicated test suite |

### Frontend Testing

| Type | Coverage | Tools |
|------|----------|-------|
| Unit | Hooks, utilities | Jest |
| Component | UI components | React Testing Library |
| E2E | User journeys | Playwright |

### Critical Test Cases

1. **Auth Flow**: Register → Login → Access protected route → Logout
2. **Token Refresh**: Access expired → Auto refresh → Continue session
3. **User Isolation**: User A cannot see/modify User B's todos
4. **CRUD Operations**: Create → Read → Update → Soft Delete → Verify hidden

---

## Security Checklist

- [ ] Passwords hashed with bcrypt (12+ rounds)
- [ ] JWT access tokens expire in 15 minutes
- [ ] Refresh tokens in HttpOnly cookies only
- [ ] All todo queries filter by user_id
- [ ] CORS configured with explicit origins
- [ ] Rate limiting on auth endpoints
- [ ] No secrets in code or logs
- [ ] Input validation on all endpoints
- [ ] SQL injection prevented (SQLModel parameterized)
- [ ] XSS prevented (React escaping, proper headers)

---

## Complexity Tracking

> No constitution violations requiring justification. All principles satisfied.

---

## Related Documents

- [Specification](./spec.md) - Feature requirements
- [Data Model](./data-model.md) - Entity definitions
- [API Contracts](./contracts/openapi.yaml) - OpenAPI specification
- [Quickstart](./quickstart.md) - Developer setup guide
- [Constitution](../../.specify/memory/constitution.md) - Governance rules
