---
id: 006
title: MUI Todoist Redesign Auto Tags
stage: green
date: 2026-02-06
surface: agent
model: claude-opus-4-6
feature: fullstack-todo-app
branch: 1-fullstack-todo-app
user: darakhshan
command: implement
labels: ["mui", "todoist", "theme", "auto-tags", "ui-redesign"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/lib/theme.ts
  - frontend/context/ThemeContext.tsx
  - backend/app/utils/auto_tags.py
  - frontend/components/layout/Sidebar.tsx
  - frontend/app/layout.tsx
  - frontend/app/globals.css
  - frontend/app/page.tsx
  - frontend/types/todo.ts
  - frontend/lib/validators.ts
  - frontend/lib/utils.ts
  - frontend/components/layout/Header.tsx
  - frontend/components/auth/AuthGuard.tsx
  - frontend/components/auth/LoginForm.tsx
  - frontend/components/auth/SignupForm.tsx
  - frontend/components/todos/TodoForm.tsx
  - frontend/components/todos/TodoItem.tsx
  - frontend/components/todos/TodoList.tsx
  - frontend/components/todos/TodoFilters.tsx
  - frontend/components/todos/TodoPagination.tsx
  - frontend/app/(auth)/login/page.tsx
  - frontend/app/(auth)/signup/page.tsx
  - frontend/app/(dashboard)/layout.tsx
  - frontend/app/(dashboard)/todos/page.tsx
  - frontend/app/(dashboard)/todos/new/page.tsx
  - frontend/app/(dashboard)/todos/[id]/page.tsx
  - frontend/app/(dashboard)/profile/page.tsx
  - frontend/hooks/useTodos.ts
  - backend/app/models/schemas.py
  - backend/app/services/todo_service.py
  - frontend/context/AuthContext.tsx
  - frontend/services/auth.service.ts
tests:
  - npm run build (PASS)
  - npm run type-check (PASS - only pre-existing e2e warnings)
---

## Prompt

Implement the following plan:

# UI Redesign: MUI + Todoist Theme + Auto-Tags

## Summary
Replace all custom Tailwind components with Material UI, add Todoist-style sidebar layout with dark/light theme toggle, and implement backend auto-tag generation from todo title/description keywords.

(Full 5-phase plan covering MUI setup, backend auto-tags, component replacement, page rewrites, and polish)

## Response snapshot

Implemented the complete 5-phase UI redesign:

**Phase 1 - MUI Setup**: Installed @mui/material, @emotion/react, @emotion/styled, @mui/icons-material. Created theme.ts with Todoist-style light/dark palettes (primary red #dc4c3e, priority colors). Created ThemeContext.tsx with localStorage-persisted dark/light toggle. Updated root layout to wrap with AppThemeProvider + CssBaseline.

**Phase 2 - Backend Auto-Tags**: Created auto_tags.py with keyword-based tag extraction (9 category maps: work, personal, finance, health, learning, tech, urgent, shopping, errands). Removed tags from TodoCreate/TodoUpdate schemas. Integrated extract_tags() into create_todo() and update_todo() service methods.

**Phase 3 - Component Replacement**: Deleted 4 custom common components (Button, Input, ErrorAlert, LoadingSpinner). Created Sidebar.tsx with Todoist-style navigation (All Todos, Today, Upcoming, priority/status filters, profile link). Rewrote Header with MUI AppBar + theme toggle + user dropdown menu. Rewrote all auth and todo components using MUI (Card, TextField, Button, Alert, Chip, Checkbox, etc).

**Phase 4 - Page Rewrites**: Dashboard layout now has permanent sidebar (desktop) + temporary drawer (mobile) + fixed AppBar. Todos page reads filters from URL query params, uses Dialog for delete confirmation, Snackbar for notifications. All pages rewritten with MUI Container, Paper, Breadcrumbs, etc.

**Phase 5 - Polish**: Updated utils.ts (removed Tailwind color helpers). Fixed pre-existing unused import issues. Build passes cleanly.

## Outcome

- ✅ Impact: Complete UI overhaul from custom Tailwind to MUI with Todoist theme, auto-tag generation, and sidebar navigation
- 🧪 Tests: npm run build PASS, type-check PASS
- 📁 Files: 3 new files, 4 deleted, 28 modified
- 🔁 Next prompts: Test signup/login flow end-to-end, verify dark/light theme toggle, test auto-tag generation with backend
- 🧠 Reflection: Large coordinated change across frontend and backend completed in single session with clean build

## Evaluation notes (flywheel)

- Failure modes observed: Pre-existing unused import errors (getAccessToken, User) blocked build until fixed
- Graders run and results (PASS/FAIL): npm run build PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Add Suspense boundaries if static generation issues arise with useSearchParams
