# Feature Specification: Full-Stack Todo Application

**Feature Branch**: `1-fullstack-todo-app`
**Created**: 2026-02-05
**Status**: Draft
**Input**: Full-Stack Todo App with FastAPI backend, Next.js frontend, JWT authentication, and PostgreSQL persistence

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Authentication (Priority: P1)

As a new user, I want to create an account and securely log in so that I can access my personal todo items from any device.

**Why this priority**: Authentication is the foundation for all other features. Without user accounts, there's no way to associate todos with specific users or ensure data privacy.

**Independent Test**: Can be fully tested by completing signup, login, and logout flows. Delivers secure user identity management.

**Acceptance Scenarios**:

1. **Given** I am a new visitor, **When** I submit valid email, username, and password on the signup form, **Then** my account is created and I receive authentication tokens to access the application.

2. **Given** I am a registered user, **When** I submit correct email and password on the login form, **Then** I receive authentication tokens and am redirected to my todo dashboard.

3. **Given** I am logged in, **When** my access token expires (within 15 minutes), **Then** the system automatically refreshes my session using the refresh token without interrupting my workflow.

4. **Given** I am logged in, **When** I click logout, **Then** my tokens are invalidated and I am redirected to the login page.

5. **Given** I am a registered user, **When** I submit an incorrect password, **Then** I see an error message "Invalid credentials" without revealing which field was wrong.

---

### User Story 2 - Todo CRUD Operations (Priority: P1)

As an authenticated user, I want to create, view, update, and delete my todo items so that I can manage my tasks effectively.

**Why this priority**: Core todo functionality is the primary value proposition of the application. Users need basic task management to derive any value.

**Independent Test**: Can be tested by creating a todo, viewing it in a list, editing its details, marking it complete, and deleting it.

**Acceptance Scenarios**:

1. **Given** I am logged in, **When** I submit a new todo with title "Buy groceries", **Then** the todo appears in my list with status "pending" and default priority "medium".

2. **Given** I have existing todos, **When** I view my todo list, **Then** I see only my todos (not other users') with title, status, priority, and due date visible.

3. **Given** I have a todo, **When** I update its status to "completed", **Then** the change is saved and reflected immediately in the UI.

4. **Given** I have a todo, **When** I delete it, **Then** it no longer appears in my active list but can be recovered within 30 days (soft delete).

5. **Given** I have multiple todos, **When** I filter by status "completed", **Then** I see only completed todos.

---

### User Story 3 - Todo List with Filtering and Pagination (Priority: P2)

As a user with many todos, I want to filter, sort, and paginate my todo list so that I can find specific tasks quickly.

**Why this priority**: Enhances usability for power users with many tasks. Basic CRUD works without this, but this improves the experience significantly.

**Independent Test**: Can be tested by creating multiple todos with different statuses/priorities, then using filters and pagination controls.

**Acceptance Scenarios**:

1. **Given** I have 50 todos, **When** I view my todo list, **Then** I see the first 20 items with pagination controls to navigate.

2. **Given** I am viewing my todos, **When** I filter by priority "high", **Then** I see only high-priority todos.

3. **Given** I am viewing my todos, **When** I sort by due date ascending, **Then** todos are ordered with earliest due dates first.

4. **Given** I am viewing filtered results, **When** I clear filters, **Then** I see all my todos again.

---

### User Story 4 - User Profile Management (Priority: P3)

As a user, I want to view and update my profile information so that I can keep my account details current.

**Why this priority**: Nice-to-have feature that improves user experience but is not essential for core task management functionality.

**Independent Test**: Can be tested by viewing profile, updating username, and verifying changes persist.

**Acceptance Scenarios**:

1. **Given** I am logged in, **When** I navigate to my profile, **Then** I see my email, username, and account creation date.

2. **Given** I am viewing my profile, **When** I update my username, **Then** the change is saved and I see a confirmation message.

3. **Given** I am viewing my profile, **When** I try to change my email to an already-registered email, **Then** I see an error message and my email remains unchanged.

---

### Edge Cases

- What happens when a user tries to access another user's todo by ID? → Returns "Not Found" (404) to prevent information disclosure.
- What happens when a user submits a todo with an empty title? → Returns validation error requiring non-empty title.
- What happens when the access token expires mid-request? → Request fails with 401, frontend auto-refreshes and retries.
- What happens when the refresh token is invalid or expired? → User is redirected to login page.
- What happens when a user creates a todo with a past due date? → Allowed, but visually flagged as overdue.
- What happens when a deleted todo is accessed? → Returns "Not Found" (404) as if it never existed.
- What happens when username contains special characters? → Only alphanumeric and underscore allowed (3-30 characters).
- What happens when password doesn't meet requirements? → Validation error specifying: minimum 8 characters, at least one uppercase, one lowercase, one number.

## Requirements *(mandatory)*

### Functional Requirements

**Authentication:**
- **FR-001**: System MUST allow users to register with email, username, and password.
- **FR-002**: System MUST validate email format and uniqueness during registration.
- **FR-003**: System MUST validate username uniqueness and format (alphanumeric + underscore, 3-30 chars).
- **FR-004**: System MUST enforce password requirements (min 8 chars, uppercase, lowercase, number).
- **FR-005**: System MUST authenticate users with email and password, returning access and refresh tokens.
- **FR-006**: System MUST issue access tokens valid for 15 minutes.
- **FR-007**: System MUST issue refresh tokens valid for 7 days, stored in HTTP-only cookies.
- **FR-008**: System MUST allow token refresh without re-authentication while refresh token is valid.
- **FR-009**: System MUST invalidate refresh tokens on logout.
- **FR-010**: System MUST hash passwords using bcrypt with minimum 12 rounds.

**Todo Management:**
- **FR-011**: System MUST allow authenticated users to create todos with title (required), description (optional), priority, due date, and tags.
- **FR-012**: System MUST assign default values: status="pending", priority="medium" for new todos.
- **FR-013**: System MUST allow users to update their own todos (title, description, status, priority, due date, tags).
- **FR-014**: System MUST support todo statuses: pending, in_progress, completed.
- **FR-015**: System MUST support todo priorities: low, medium, high.
- **FR-016**: System MUST implement soft delete for todos (retained for 30 days).
- **FR-017**: System MUST ensure users can only access their own todos (strict user isolation).
- **FR-018**: System MUST return 404 Not Found when accessing non-existent or other users' todos.

**Listing and Filtering:**
- **FR-019**: System MUST return paginated todo lists (default 20 items per page).
- **FR-020**: System MUST support filtering todos by status.
- **FR-021**: System MUST support filtering todos by priority.
- **FR-022**: System MUST support sorting todos by created_at, due_date, or priority.
- **FR-023**: System MUST exclude soft-deleted todos from normal queries.

**User Profile:**
- **FR-024**: System MUST allow users to view their profile (email, username, created_at).
- **FR-025**: System MUST allow users to update their username (with uniqueness validation).
- **FR-026**: System MUST NOT allow email changes (for security/identity reasons).

**System:**
- **FR-027**: System MUST provide a health check endpoint for monitoring.
- **FR-028**: System MUST return consistent response format for all API endpoints.
- **FR-029**: System MUST include timestamps (ISO8601) in all responses.
- **FR-030**: System MUST log security events (login attempts, failed authentications).

### Key Entities

- **User**: Represents an authenticated account holder. Has unique email and username, hashed password, and audit timestamps. Each user owns zero or more todos.

- **Todo**: Represents a task item belonging to a user. Contains title (required), description, status (pending/in_progress/completed), priority (low/medium/high), optional due date, optional tags (list of strings), and soft-delete timestamp. Always linked to exactly one user.

### Data Schema

**User:**
- Unique identifier (UUID)
- Email (unique, max 255 characters)
- Username (unique, 3-30 alphanumeric + underscore)
- Password hash (bcrypt)
- Created at (timestamp with timezone)
- Updated at (timestamp with timezone)
- Deleted at (nullable, for soft delete)

**Todo:**
- Unique identifier (UUID)
- Owner user identifier (foreign key)
- Title (required, max 255 characters)
- Description (optional, text)
- Status (enum: pending, in_progress, completed)
- Priority (enum: low, medium, high)
- Due date (optional, timestamp with timezone)
- Tags (list of strings, stored as JSON)
- Created at (timestamp with timezone)
- Updated at (timestamp with timezone)
- Deleted at (nullable, for soft delete)

### API Response Format

All API endpoints MUST return responses in this consistent format:

**Success Response:**
```
{
  "success": true,
  "data": <object or array>,
  "error": null,
  "timestamp": "<ISO8601>"
}
```

**Error Response:**
```
{
  "success": false,
  "data": null,
  "error": "<error message>",
  "timestamp": "<ISO8601>"
}
```

**Paginated Response (for list endpoints):**
```
{
  "success": true,
  "data": {
    "items": [...],
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  },
  "error": null,
  "timestamp": "<ISO8601>"
}
```

### API Endpoints Summary

| Method | Endpoint | Description | Auth Required |
| ------ | -------- | ----------- | ------------- |
| POST | /auth/signup | Create new user account | No |
| POST | /auth/login | Authenticate and get tokens | No |
| POST | /auth/refresh | Get new access token | Refresh Token |
| POST | /auth/logout | Invalidate refresh token | Access Token |
| GET | /todos | List user's todos (paginated) | Access Token |
| POST | /todos | Create new todo | Access Token |
| GET | /todos/{id} | Get single todo | Access Token |
| PATCH | /todos/{id} | Update todo | Access Token |
| DELETE | /todos/{id} | Soft delete todo | Access Token |
| GET | /users/me | Get current user profile | Access Token |
| PATCH | /users/me | Update current user profile | Access Token |
| GET | /health | Health check | No |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete registration and login within 30 seconds on first attempt.
- **SC-002**: Users can create a new todo in under 5 seconds from dashboard.
- **SC-003**: Todo list loads within 2 seconds for users with up to 1000 todos.
- **SC-004**: System handles 100 concurrent users without degradation (response times remain under 2 seconds).
- **SC-005**: Zero unauthorized data access - users can never see or modify other users' todos.
- **SC-006**: Session remains active for 7 days without requiring re-login (via automatic token refresh).
- **SC-007**: 100% of form validation errors display clear, actionable messages to users.
- **SC-008**: System availability of 99.9% during normal operations.
- **SC-009**: All deleted todos are recoverable within the 30-day retention period.
- **SC-010**: Mobile users (< 640px viewport) can complete all core tasks without horizontal scrolling.

## Assumptions

1. **Single-tenant deployment**: Each deployment serves one organization; multi-tenancy is not required.
2. **Email verification not required**: Users can log in immediately after registration (no email confirmation step).
3. **No password reset flow**: Out of scope for initial release; users contact support for account recovery.
4. **No social login**: Only email/password authentication; OAuth providers not included.
5. **English only**: No internationalization required for initial release.
6. **Tags are free-form**: No predefined tag taxonomy; users create tags as needed.
7. **No recurring todos**: Each todo is a one-time item; recurring task patterns not supported.
8. **No todo sharing**: Todos are strictly private to the owning user.
9. **No file attachments**: Todos contain only text data.
10. **Timezone handling**: All dates stored in UTC; frontend converts to user's local timezone for display.

## Out of Scope

- Email verification and password reset flows
- Social authentication (Google, GitHub, etc.)
- Team/workspace features and todo sharing
- File attachments on todos
- Recurring/repeating todos
- Mobile native applications (web responsive only)
- Offline functionality
- Real-time collaboration/sync
- Todo templates
- Subtasks/nested todos
- Time tracking
- Notifications and reminders
