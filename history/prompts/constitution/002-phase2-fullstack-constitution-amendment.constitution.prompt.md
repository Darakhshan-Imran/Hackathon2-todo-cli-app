---
id: 002
title: Phase 2 Fullstack Constitution Amendment
stage: constitution
date: 2026-02-05
surface: agent
model: claude-opus-4-5-20251101
feature: fullstack-todo-app
branch: main
user: developer
command: /sp.constitution
labels: ["constitution", "phase-2", "fullstack", "fastapi", "nextjs", "jwt", "postgresql"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution document, no code tests)
---

## Prompt

in current constitution.md future phases are declared just extend them and update constitution.md and marked phase 1 as completed. these are the phase 2 description Create constitutional principles for a Full-Stack Todo App (Phase 2) that extends a Phase 1 CLI implementation into a production web application.

Requirements:
1. Backend: FastAPI + SQLModel ORM + Neon PostgreSQL + JWT Authentication
2. Frontend: Next.js + Tailwind CSS + React Hooks
3. Database: User-Todo relationship with strict data isolation
4. Auth: JWT access/refresh token pattern (15min access, 7day refresh)
5. Security: Bcrypt password hashing, stateless auth, HttpOnly cookies

Constitutional Rules MUST Cover:
- JWT token strategy (access/refresh separation, claims structure)
- User isolation (service layer enforcement, no cross-user data access)
- Security standards (password hashing rounds, HTTPS, CORS config)
- FastAPI architecture (async/await, dependency injection)
- Database & ORM (SQLModel, connection pooling for Neon)
- Frontend authentication flow (token storage, auto-refresh)
- UI/UX standards (Tailwind CSS, responsive design, accessibility)
- API contract (RESTful endpoints, consistent response format)
- Data persistence (User/Todo entity definitions with constraints)
- Testing principles (unit, integration, E2E coverage)
- Environment configuration (backend/frontend env vars)
- Deployment readiness (Docker, production considerations)
- Migration path from Phase 1 (reuse domain logic, preserve CLI)

Output Format: Establish binding rules for Phase 2, covering all 12+ principles with specific technical requirements, acceptance criteria, and compliance checklist.

## Response snapshot

Updated constitution from version 1.0.0 to 1.1.0 with comprehensive Phase 2 principles:

**Added Sections:**
- Phase Completion Status table (Phase 1 marked COMPLETED)
- 14 new Phase 2 Principles (XIV-XXVII) covering:
  - XIV. JWT Token Strategy (15min access, 7day refresh, rotation, HttpOnly cookies)
  - XV. User Data Isolation (service layer enforcement, 404 on cross-user access)
  - XVI. Security Standards (bcrypt 12+ rounds, CORS, rate limiting, HTTPS)
  - XVII. FastAPI Architecture (async/await, dependency injection, OpenAPI)
  - XVIII. Database and ORM Standards (SQLModel, Neon pooling, Alembic migrations)
  - XIX. Frontend Authentication Flow (memory-only tokens, auto-refresh)
  - XX. UI/UX Standards (Tailwind CSS, WCAG 2.1 AA, dark mode)
  - XXI. API Contract Standards (REST conventions, consistent response format)
  - XXII. Data Persistence Schema (User and Todo entity definitions)
  - XXIII. Testing Principles (unit 80%, integration, E2E)
  - XXIV. Environment Configuration (backend/frontend env vars)
  - XXV. Deployment Readiness (Docker, health checks, graceful shutdown)
  - XXVI. Migration Path from Phase 1 (preserve CLI, reuse domain logic)
  - XXVII. TypeScript Standards (strict mode, Zod validation)
- Phase 2 Compliance Checklist (38 verification items)
- Updated Technology Stack with Phase 2 backend and frontend specifics
- New Agent Skills for Phase 2 (auth.jwt, auth.password, db.sqlmodel, api.rest, frontend.auth)

## Outcome

- ✅ Impact: Constitution extended with 14 binding Phase 2 principles, Phase 1 marked complete
- 🧪 Tests: N/A (governance document)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: /sp.specify to create Phase 2 feature specification for fullstack-todo-app
- 🧠 Reflection: All 13+ required rules covered with specific technical requirements; compliance checklist provides verification criteria

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review PASS - all requirements addressed with specific technical constraints
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - Phase 2 constitution amendment complete
