<!--
  ============================================================================
  SYNC IMPACT REPORT
  ============================================================================
  Version Change: 1.0.0 → 1.1.0

  Modified Principles: None (original 13 principles unchanged)

  Added Sections:
  - Phase Completion Status (tracking completed phases)
  - Phase 2 Principles (14 new principles for fullstack-todo-app)
  - Phase 2 Technology Stack specifics
  - Phase 2 Compliance Checklist

  Updated Sections:
  - Phase Evolution Roadmap (Phase 1 marked COMPLETED)
  - Technology Stack (added Phase 2 current stack)
  - Reusable Intelligence Requirements (added Phase 2 agents/skills)

  Removed Sections: None

  Templates Requiring Updates:
  - ✅ plan-template.md - Compatible (Constitution Check section exists)
  - ✅ spec-template.md - Compatible (Requirements section aligns)
  - ✅ tasks-template.md - Compatible (Phase structure aligns)

  Follow-up TODOs: None
  ============================================================================
-->

# Todo System Constitution

## Purpose

Define permanent architectural, behavioral, and governance rules for a multi-phase evolving Todo system, starting from a Python CLI app and evolving into a cloud-native, AI-powered distributed system.

## Phase Completion Status

| Phase | Name | Status | Completion Date |
|-------|------|--------|-----------------|
| 1 | CLI + In-Memory | ✅ COMPLETED | 2026-02-05 |
| 2 | Fullstack Web App | 🔄 CURRENT | - |
| 3 | Web UI + Chatbot (EN/UR) | ⏳ PLANNED | - |
| 4 | Voice + Cloud-Native | ⏳ PLANNED | - |

---

## Core Principles (All Phases)

### I. Spec-Driven Development Only

All development MUST follow Spec-Driven Development (SDD) methodology. No "vibe coding" or ad-hoc implementation is permitted.

- Every feature MUST have a specification before implementation begins
- Specifications MUST be reviewed and approved before coding
- Implementation MUST trace back to specification requirements
- Deviations from spec require explicit amendment and re-approval

### II. Reusable Intelligence Architecture

Claude Code MUST operate using reusable intelligence via Subagents and Agent Skills.

- All AI-assisted operations MUST use defined Subagents
- Agent Skills MUST be designed for reuse across all project phases
- Intelligence components MUST be documented and versioned
- No ad-hoc AI prompts in production workflows

### III. Cloud-Native Blueprints

Cloud-Native Blueprints MUST be defined via Agent Skills, even if not implemented in Phase 1.

- Infrastructure patterns MUST be declared as Agent Skills
- Cloud deployment configurations MUST be version-controlled
- Migration paths from CLI to cloud MUST be documented
- Serverless, container, and orchestration patterns MUST be pre-defined

### IV. Python Standards

Python version MUST be 3.13 or higher. Use `uv` as the package and environment manager.

- All code MUST be compatible with Python 3.13+
- `uv` is the ONLY permitted package manager
- Virtual environments MUST be managed via `uv`
- Dependencies MUST be declared in `pyproject.toml`
- Lock files MUST be committed to version control

### V. Clean Code Architecture

Follow clean code principles and maintain a readable project structure.

- Code MUST be self-documenting with clear naming conventions
- Functions MUST do one thing and do it well
- Modules MUST have single responsibility
- Directory structure MUST reflect domain boundaries
- No circular dependencies permitted

### VI. Phase 1 Storage Constraint

Phase 1 MUST store data in memory only—no files, no database.

- All todo items MUST persist only for session duration
- No file I/O for data persistence in Phase 1
- No database connections in Phase 1
- Data structures MUST be designed for future persistence migration

### VII. Language Standards

English is the default language. Urdu language support MUST be planned for chatbot interaction in future phases.

- All code, comments, and documentation MUST be in English
- User-facing messages in Phase 1 MUST be in English
- Internationalization (i18n) architecture MUST be planned
- Urdu chatbot integration is a declared future capability

### VIII. Voice Command Declaration

Voice command support MUST be declared in the constitution but NOT implemented in Phase 1.

- Voice interface is a declared future capability
- API boundaries MUST accommodate future voice input
- Command structure MUST be voice-friendly (clear, unambiguous)
- No voice-related dependencies in Phase 1

### IX. Modular Extensibility

All logic MUST be modular and future-extensible.

- Business logic MUST be separate from I/O handling
- Features MUST be pluggable without core changes
- Interfaces MUST be stable; implementations may vary
- Extension points MUST be documented

### X. Security-First Mindset

Security-first mindset MUST be followed even in CLI phase.

- Input validation MUST occur at all entry points
- No sensitive data in logs or error messages
- Command injection prevention is mandatory
- Authentication/authorization patterns MUST be planned (even if not enforced in Phase 1)

### XI. Test-First Development

Test-Driven Development (TDD) is MANDATORY for all feature implementation.

- Tests MUST be written before implementation code
- Tests MUST fail before implementation begins
- Red-Green-Refactor cycle MUST be strictly followed
- Minimum 80% code coverage required

### XII. Observability

All operations MUST be observable and debuggable.

- Structured logging MUST be implemented
- Error states MUST be clearly reported
- CLI output MUST support both human-readable and JSON formats
- Debug mode MUST expose internal state

### XIII. Simplicity (YAGNI)

Start simple. Do not build features that are not immediately needed.

- Implement the simplest solution that satisfies requirements
- No speculative features or over-engineering
- Complexity MUST be justified in writing
- Prefer deletion over deprecation

---

## Phase 2 Principles (Fullstack Todo App)

Phase 2 extends the CLI application into a production-ready fullstack web application with user authentication and data persistence.

### XIV. JWT Token Strategy

Stateless authentication MUST use JWT access/refresh token pattern.

- Access tokens MUST expire in 15 minutes maximum
- Refresh tokens MUST expire in 7 days maximum
- Access token claims MUST include: `sub` (user_id), `exp`, `iat`, `type: "access"`
- Refresh token claims MUST include: `sub` (user_id), `exp`, `iat`, `type: "refresh"`, `jti` (unique token ID)
- Refresh tokens MUST be rotated on each use (invalidate old, issue new)
- Token signing MUST use RS256 or HS256 with minimum 256-bit secret
- Access tokens MUST be transmitted via Authorization header: `Bearer <token>`
- Refresh tokens MUST be stored in HttpOnly, Secure, SameSite=Strict cookies

### XV. User Data Isolation

Strict user isolation MUST be enforced at the service layer.

- Every database query for user-owned resources MUST include `user_id` filter
- Service layer MUST receive `current_user` from dependency injection, never from request body
- Cross-user data access MUST result in 404 Not Found (not 403) to prevent enumeration
- Admin endpoints (if any) MUST have separate authorization middleware
- All todo operations MUST validate ownership: `todo.user_id == current_user.id`
- Unit tests MUST verify isolation by attempting cross-user access

### XVI. Security Standards

Production-grade security MUST be implemented from day one.

- Password hashing MUST use bcrypt with minimum 12 rounds
- HTTPS MUST be enforced in production (HTTP redirect to HTTPS)
- CORS MUST be configured with explicit allowed origins (no wildcards in production)
- Rate limiting MUST be implemented: 100 requests/minute per IP for auth endpoints
- SQL injection prevention via parameterized queries (SQLModel handles this)
- XSS prevention via proper content-type headers and input sanitization
- CSRF protection via SameSite cookies and Origin validation
- Secrets MUST be loaded from environment variables, never hardcoded
- `.env` files MUST be in `.gitignore`

### XVII. FastAPI Architecture

Backend MUST follow FastAPI best practices with async/await patterns.

- All database operations MUST be async (using async SQLAlchemy/SQLModel)
- Dependency injection MUST be used for: database sessions, current user, configuration
- Pydantic models MUST define all request/response schemas
- API versioning MUST use URL prefix: `/api/v1/`
- Exception handlers MUST return consistent error response format
- Background tasks MUST use FastAPI BackgroundTasks or Celery for long-running operations
- OpenAPI documentation MUST be auto-generated and accurate

### XVIII. Database and ORM Standards

SQLModel with Neon PostgreSQL MUST be the persistence layer.

- SQLModel MUST be used as the ORM (combines SQLAlchemy + Pydantic)
- Connection pooling MUST be configured for Neon serverless (use `pool_size=5`, `max_overflow=10`)
- All models MUST inherit from SQLModel base
- Migrations MUST use Alembic with auto-generated migration scripts
- Foreign key constraints MUST be defined for all relationships
- Indexes MUST be created for: `user_id` on todos, `email` on users
- Soft delete MUST be implemented via `deleted_at` timestamp (nullable)
- Timestamps MUST be UTC and include `created_at`, `updated_at` on all entities

### XIX. Frontend Authentication Flow

Next.js frontend MUST implement secure token management.

- Access tokens MUST be stored in memory only (React state/context), never localStorage
- Refresh tokens MUST be in HttpOnly cookies (set by backend)
- Token refresh MUST happen automatically before access token expiry (e.g., at 14 minutes)
- Failed refresh MUST redirect to login page
- Auth context MUST provide: `user`, `isAuthenticated`, `login()`, `logout()`, `isLoading`
- Protected routes MUST use middleware or higher-order component pattern
- Login/register forms MUST validate client-side before submission
- Loading states MUST be shown during auth operations

### XX. UI/UX Standards

Frontend MUST follow modern UI/UX principles with Tailwind CSS.

- Tailwind CSS MUST be the primary styling solution (no custom CSS unless necessary)
- Responsive design MUST support: mobile (< 640px), tablet (640-1024px), desktop (> 1024px)
- Accessibility MUST meet WCAG 2.1 AA standards:
  - All interactive elements MUST have focus states
  - Color contrast MUST be minimum 4.5:1
  - All images MUST have alt text
  - Forms MUST have proper labels and ARIA attributes
- Dark mode MUST be supported via Tailwind's dark variant
- Loading skeletons MUST be shown during data fetches
- Error states MUST be clearly communicated with actionable messages
- Toast notifications MUST be used for async operation feedback

### XXI. API Contract Standards

RESTful API design MUST follow consistent patterns.

- Endpoints MUST follow REST conventions:
  - `GET /api/v1/todos` - list todos (with pagination)
  - `POST /api/v1/todos` - create todo
  - `GET /api/v1/todos/{id}` - get single todo
  - `PUT /api/v1/todos/{id}` - update todo
  - `DELETE /api/v1/todos/{id}` - delete todo
- Response format MUST be consistent:
  ```json
  {
    "data": {...} | [...],
    "meta": {"page": 1, "total": 100, "per_page": 20},
    "error": null
  }
  ```
- Error response format MUST be:
  ```json
  {
    "data": null,
    "error": {"code": "VALIDATION_ERROR", "message": "...", "details": [...]}
  }
  ```
- HTTP status codes MUST be semantic: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 404 Not Found, 422 Unprocessable Entity, 500 Internal Server Error
- Pagination MUST use query params: `?page=1&per_page=20`

### XXII. Data Persistence Schema

User and Todo entities MUST follow defined schema.

**User Entity:**
- `id`: UUID, primary key
- `email`: string, unique, indexed, max 255 chars
- `password_hash`: string, bcrypt hash
- `created_at`: timestamp with timezone, default now()
- `updated_at`: timestamp with timezone, auto-update
- `deleted_at`: timestamp with timezone, nullable (soft delete)

**Todo Entity:**
- `id`: UUID, primary key
- `user_id`: UUID, foreign key → users.id, indexed
- `title`: string, max 255 chars, required
- `description`: text, optional
- `status`: enum (pending, in_progress, completed), default pending
- `priority`: enum (low, medium, high), default medium
- `due_date`: timestamp with timezone, optional
- `created_at`: timestamp with timezone, default now()
- `updated_at`: timestamp with timezone, auto-update
- `deleted_at`: timestamp with timezone, nullable (soft delete)

### XXIII. Testing Principles

Comprehensive testing MUST cover all layers.

- Unit tests MUST cover: models, services, utilities (80% minimum coverage)
- Integration tests MUST cover: API endpoints with database
- E2E tests MUST cover: critical user journeys (login, create todo, complete todo)
- Backend tests MUST use pytest with async fixtures
- Frontend tests MUST use Jest + React Testing Library
- E2E tests MUST use Playwright or Cypress
- Test database MUST be isolated (separate from dev/prod)
- CI pipeline MUST run all tests before merge

### XXIV. Environment Configuration

Environment variables MUST be properly managed.

**Backend (.env):**
- `DATABASE_URL`: Neon PostgreSQL connection string
- `JWT_SECRET_KEY`: minimum 256-bit secret for token signing
- `JWT_ALGORITHM`: RS256 or HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES`: default 15
- `REFRESH_TOKEN_EXPIRE_DAYS`: default 7
- `CORS_ORIGINS`: comma-separated allowed origins
- `ENVIRONMENT`: development | staging | production

**Frontend (.env.local):**
- `NEXT_PUBLIC_API_URL`: backend API base URL
- `NEXT_PUBLIC_ENVIRONMENT`: development | staging | production

### XXV. Deployment Readiness

Production deployment MUST follow containerization standards.

- Backend MUST have Dockerfile with multi-stage build
- Frontend MUST have Dockerfile or use Vercel deployment
- Docker Compose MUST define local development environment
- Health check endpoint MUST exist: `GET /api/v1/health`
- Database migrations MUST run automatically on deployment
- Environment-specific configurations MUST use environment variables
- Logging MUST be structured JSON in production
- Graceful shutdown MUST be implemented for all services

### XXVI. Migration Path from Phase 1

Phase 2 MUST preserve and extend Phase 1 capabilities.

- CLI application MUST remain functional (separate package in `cli-todo-app/`)
- Domain logic from Phase 1 MUST be reusable in Phase 2 services
- Todo model extensions MUST be backward compatible
- API MUST expose all CLI operations plus authentication
- Existing tests MUST continue to pass
- Documentation MUST reference Phase 1 for context

### XXVII. TypeScript Standards (Frontend)

Next.js frontend MUST use TypeScript with strict configuration.

- `strict: true` MUST be enabled in tsconfig.json
- All components MUST have typed props interfaces
- API responses MUST have corresponding TypeScript types
- `any` type MUST NOT be used (use `unknown` with type guards instead)
- Shared types MUST be in dedicated `types/` directory
- Form validation MUST use Zod with TypeScript inference

---

## Reusable Intelligence Requirements

### Subagents

The following Subagents MUST be defined and available:

| Subagent | Purpose | Phase |
|----------|---------|-------|
| Domain Logic Agent | Execute todo business logic operations | 1+ |
| Spec Validation Agent | Validate specifications against constitution | 1+ |
| Code Quality Agent | Enforce clean code standards | 1+ |
| Test Generation Agent | Generate test cases from specifications | 1+ |
| Cloud Mapping Agent | Map features to cloud-native patterns | 2+ |
| Auth Security Agent | Validate JWT and security implementations | 2+ |
| API Contract Agent | Validate REST API consistency | 2+ |
| i18n Agent | Handle internationalization concerns | 3+ |

### Agent Skills

The following Agent Skills MUST be defined and reusable:

| Skill | Description | Phase Available |
|-------|-------------|-----------------|
| `todo.domain` | Todo CRUD operations, priority, tags, due dates | 1+ |
| `todo.validate` | Input validation and business rule enforcement | 1+ |
| `spec.validate` | Specification conformance checking | 1+ |
| `code.structure` | Clean Python project structure enforcement | 1+ |
| `code.quality` | Code quality and style checking | 1+ |
| `auth.jwt` | JWT token generation, validation, refresh | 2+ |
| `auth.password` | Bcrypt hashing and verification | 2+ |
| `db.sqlmodel` | SQLModel ORM patterns and migrations | 2+ |
| `api.rest` | RESTful endpoint patterns | 2+ |
| `frontend.auth` | React auth context and token management | 2+ |
| `cloud.blueprint` | Cloud-native architecture patterns | Declared (impl 2+) |
| `cloud.deploy` | Deployment configuration generation | Declared (impl 2+) |
| `i18n.urdu` | Urdu language support for chatbot | Declared (impl 3+) |
| `voice.command` | Voice command parsing and routing | Declared (impl 4+) |

---

## Technology Stack

### Phase 1 (COMPLETED ✅)

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Language | Python 3.13+ | Modern features, type hints, performance |
| Package Manager | uv | Fast, reliable, lockfile support |
| Interface | CLI (argparse/click) | Simple, testable, scriptable |
| Storage | In-memory (dict/dataclass) | Phase constraint |
| Testing | pytest | Industry standard, excellent fixtures |
| Linting | ruff | Fast, comprehensive, replaces multiple tools |
| Type Checking | mypy | Static type verification |

### Phase 2 (CURRENT 🔄)

**Backend:**

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Language | Python 3.13+ | Consistency with Phase 1 |
| Framework | FastAPI | Async, modern, auto-docs, type hints |
| ORM | SQLModel | Combines SQLAlchemy + Pydantic |
| Database | Neon PostgreSQL | Serverless, scalable, branching |
| Authentication | JWT (PyJWT) | Stateless, scalable |
| Password Hashing | bcrypt (passlib) | Industry standard, configurable rounds |
| Migrations | Alembic | SQLAlchemy-compatible |
| Testing | pytest + pytest-asyncio | Async test support |

**Frontend:**

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Framework | Next.js 14+ | App Router, RSC, API routes |
| Language | TypeScript | Type safety, developer experience |
| Styling | Tailwind CSS | Utility-first, responsive, dark mode |
| State | React Context + Hooks | Simple, built-in, sufficient for auth |
| Forms | React Hook Form + Zod | Validation, type inference |
| HTTP Client | Fetch API / Axios | Native or feature-rich option |
| Testing | Jest + RTL + Playwright | Unit, component, E2E |

### Future Phases (Declared)

| Phase | Additions | Notes |
|-------|-----------|-------|
| 3 | i18n, Urdu chatbot, Web UI enhancements | Localization layer |
| 4 | Voice SDK, Cloud deployment (AWS/GCP) | Voice commands, production infrastructure |

---

## Phase Evolution Roadmap

```
Phase 1: CLI + In-Memory ✅ COMPLETED
    ↓
Phase 2: Fullstack Web App (CURRENT)
    ├── Backend: FastAPI + SQLModel + Neon PostgreSQL + JWT
    └── Frontend: Next.js + Tailwind + React Hooks
    ↓
Phase 3: Web UI + Chatbot (EN/UR)
    ↓
Phase 4: Voice + Cloud-Native
```

Each phase MUST:
- Maintain backward compatibility with previous phase CLI
- Pass all existing tests before adding new features
- Update specifications before implementation
- Document migration path from previous phase

---

## Phase 2 Compliance Checklist

Before Phase 2 implementation is considered complete, ALL items MUST be verified:

### Authentication
- [ ] JWT access tokens expire in ≤ 15 minutes
- [ ] JWT refresh tokens expire in ≤ 7 days
- [ ] Refresh token rotation implemented
- [ ] HttpOnly cookies used for refresh tokens
- [ ] Password hashing uses bcrypt with ≥ 12 rounds

### Security
- [ ] CORS configured with explicit origins
- [ ] Rate limiting on auth endpoints
- [ ] No secrets in codebase or logs
- [ ] HTTPS enforced in production config

### User Isolation
- [ ] All todo queries filter by user_id
- [ ] Cross-user access returns 404
- [ ] Unit tests verify isolation

### API
- [ ] All endpoints follow REST conventions
- [ ] Consistent response format implemented
- [ ] Pagination implemented for list endpoints
- [ ] OpenAPI documentation generated

### Database
- [ ] SQLModel models match schema definition
- [ ] Alembic migrations configured
- [ ] Indexes on user_id and email
- [ ] Soft delete implemented

### Frontend
- [ ] Access tokens in memory only
- [ ] Automatic token refresh implemented
- [ ] Protected routes configured
- [ ] Responsive design (mobile/tablet/desktop)
- [ ] Accessibility basics met (focus, contrast, labels)

### Testing
- [ ] Backend unit tests ≥ 80% coverage
- [ ] API integration tests exist
- [ ] Frontend component tests exist
- [ ] E2E tests for critical paths

### Deployment
- [ ] Dockerfile exists for backend
- [ ] Health check endpoint works
- [ ] Environment variables documented
- [ ] Docker Compose for local dev

---

## Governance

### Amendment Process

1. Proposed amendments MUST be documented with rationale
2. Amendments MUST be reviewed against existing principles
3. Breaking changes require MAJOR version bump
4. All amendments MUST include migration guidance

### Versioning Policy

- **MAJOR**: Backward-incompatible principle changes or removals
- **MINOR**: New principles, sections, or material expansions
- **PATCH**: Clarifications, typos, non-semantic refinements

### Compliance

- All pull requests MUST verify constitution compliance
- Complexity additions MUST be justified in PR description
- Constitution Check in plan.md MUST pass before implementation
- Violations block merge until resolved or constitution amended

### Authoritative Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Constitution | `.specify/memory/constitution.md` | Permanent rules (this file) |
| Specifications | `specs/<feature>/spec.md` | Feature requirements |
| Plans | `specs/<feature>/plan.md` | Implementation design |
| Tasks | `specs/<feature>/tasks.md` | Executable work items |
| ADRs | `history/adr/` | Architectural decisions |
| PHRs | `history/prompts/` | Prompt history records |

**Version**: 1.1.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-02-05
