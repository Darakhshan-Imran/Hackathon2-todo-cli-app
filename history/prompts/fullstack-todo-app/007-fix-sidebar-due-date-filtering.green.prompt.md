---
id: 007
title: Fix sidebar due date filtering
stage: green
date: 2026-02-06
surface: agent
model: claude-opus-4-6
feature: fullstack-todo-app
branch: 1-fullstack-todo-app
user: darakhshan
command: prompt
labels: ["bug-fix", "filtering", "sidebar", "due-date", "frontend", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/api/v1/todos.py
  - backend/app/services/todo_service.py
  - frontend/types/todo.ts
  - frontend/app/(dashboard)/todos/page.tsx
  - frontend/components/layout/Sidebar.tsx
tests:
  - Manual testing verified sidebar All Todos Today and Upcoming filters return correct results
---

## Prompt

I have tested frontend and backend both are working. There is an issue in frontend in the sidebar we have filters "ALL Todos", "Upcoming", "Todays" but only all todos are fetched on each button, however there must be filtering on the basis of upcomming and todays as well.

## Response snapshot

Fixed full-stack due date filtering across both backend and frontend. The sidebar was sending due=today and due=upcoming URL params but neither the frontend page nor backend API processed them.

Backend changes:
- Added due query parameter (Optional[str]) to the GET /todos endpoint in backend/app/api/v1/todos.py
- Implemented date-based filtering logic in backend/app/services/todo_service.py: due=today filters todos with due dates within today UTC, due=upcoming filters todos with due dates after today

Frontend changes:
- Added due field to TodoListParams type in frontend/types/todo.ts
- Updated TodosPage component in frontend/app/(dashboard)/todos/page.tsx to read the due search parameter from the URL and pass it through the useTodos hook; also updated the page title dynamically based on the active filter
- Fixed Sidebar.tsx in frontend/components/layout/Sidebar.tsx isActive logic to correctly highlight the active filter by accounting for the due query parameter

## Outcome

- Impact: Sidebar filter buttons now correctly filter todos by due date (today, upcoming, all). Users can navigate between filters and see the appropriate subset of their todos.
- Tests: Manual testing confirmed all three filter modes return correct results from the backend and display properly in the frontend.
- Files: 5 files modified (2 backend, 3 frontend)
- Next prompts: Consider adding unit tests for the date filtering logic in todo_service.py; consider adding Overdue filter for past-due todos.
- Reflection: The root cause was that the frontend was already constructing the correct URL params for sidebar navigation, but neither layer (API endpoint nor service) was wired to consume them. A straightforward end-to-end wiring fix.

## Evaluation notes (flywheel)

- Failure modes observed: URL params were being sent but silently ignored by both frontend page component and backend API, resulting in no error but incorrect behavior (all todos always returned).
- Graders run and results (PASS/FAIL): Manual verification PASS - all three sidebar filters return correct filtered results.
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add automated integration tests for the due date filtering endpoint to prevent regression.
