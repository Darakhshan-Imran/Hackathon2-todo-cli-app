# Research: Full-Stack Todo Application

**Feature**: `1-fullstack-todo-app`
**Date**: 2026-02-05
**Phase**: 0 (Research)

## Technology Decisions

### 1. Backend Framework: FastAPI

**Decision**: Use FastAPI 0.104+ with async/await patterns

**Rationale**:
- Native async support for high concurrency
- Automatic OpenAPI documentation generation
- Pydantic integration for request/response validation
- Type hints throughout for better IDE support
- Constitution mandates FastAPI (Principle XVII)

**Alternatives Considered**:
- Django REST Framework: More batteries included but synchronous by default
- Flask: Lighter but requires more boilerplate for async operations

### 2. ORM: SQLModel

**Decision**: Use SQLModel for database operations

**Rationale**:
- Combines SQLAlchemy + Pydantic in single model definition
- Same model works for DB and API schemas
- Async support via SQLAlchemy 2.0 engine
- Constitution mandates SQLModel (Principle XVIII)

**Alternatives Considered**:
- SQLAlchemy only: More flexible but requires separate Pydantic models
- Tortoise ORM: Good async support but less mature ecosystem

### 3. Database: Neon PostgreSQL

**Decision**: Use Neon serverless PostgreSQL

**Rationale**:
- Serverless scaling for variable workloads
- Full PostgreSQL compatibility (JSONB, indexes, constraints)
- Built-in connection pooling for serverless
- Constitution mandates Neon (Principle XVIII)

**Configuration**:
```python
# Neon serverless requires specific pooling config
engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections every 30 min
)
```

### 4. Authentication: JWT with HS256

**Decision**: JWT tokens with HS256 signing algorithm

**Rationale**:
- Stateless authentication scales horizontally
- HS256 simpler than RS256 for single-service architecture
- Access/refresh token pattern provides security with UX balance
- Constitution mandates JWT (Principle XIV)

**Token Configuration**:
| Token Type | Expiry | Storage | Claims |
|------------|--------|---------|--------|
| Access | 15 minutes | Memory (frontend) | sub, type, exp, iat |
| Refresh | 7 days | HttpOnly cookie | sub, type, jti, exp, iat |

### 5. Password Hashing: bcrypt

**Decision**: bcrypt with 12 rounds

**Rationale**:
- Industry standard for password hashing
- Configurable work factor for future-proofing
- Built-in salt generation prevents rainbow table attacks
- Constitution mandates bcrypt 12+ (Principle XVI)

**Implementation**: passlib[bcrypt] library with CryptContext

### 6. Frontend Framework: Next.js 14

**Decision**: Next.js 14 with App Router

**Rationale**:
- React Server Components for improved performance
- Built-in routing with layouts and nested routes
- TypeScript first-class support
- Constitution mandates Next.js (Phase 2 stack)

**Features Used**:
- App Router (not Pages Router)
- Client Components for interactive UI
- Route Groups for auth/dashboard separation
- Middleware for route protection

### 7. Styling: Tailwind CSS

**Decision**: Tailwind CSS with dark mode support

**Rationale**:
- Utility-first approach enables rapid development
- Built-in responsive utilities
- Dark mode via class strategy
- Constitution mandates Tailwind (Principle XX)

### 8. HTTP Client: Axios

**Decision**: Axios for frontend API communication

**Rationale**:
- Request/response interceptors for JWT handling
- Automatic JSON parsing
- Better error handling than native fetch
- Wide ecosystem support and documentation

**Configuration**:
- Base URL from environment variable
- Request interceptor: attach Bearer token from memory
- Response interceptor: handle 401, trigger token refresh

### 9. Form Handling: React Hook Form + Zod

**Decision**: React Hook Form with Zod validation

**Rationale**:
- Performance: uncontrolled inputs reduce re-renders
- TypeScript integration with Zod inference
- Declarative validation schemas
- Constitution mandates Zod (Principle XXVII)

---

## Best Practices Research

### FastAPI Async Patterns

```python
# Use async context managers for DB sessions
async with get_session() as session:
    result = await session.execute(query)

# Use dependency injection for authentication
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
) -> User:
    payload = verify_token(token)
    user = await session.get(User, payload["sub"])
    if not user:
        raise HTTPException(status_code=401)
    return user
```

### User Isolation Pattern

```python
# CRITICAL: ALL queries must include user_id filter
async def get_todos(user_id: UUID, session: AsyncSession) -> list[Todo]:
    query = select(Todo).where(
        Todo.user_id == user_id,
        Todo.deleted_at.is_(None)
    )
    result = await session.execute(query)
    return result.scalars().all()

# Return 404 for cross-user access (not 403)
async def get_todo(todo_id: UUID, user_id: UUID, session: AsyncSession) -> Todo:
    todo = await session.get(Todo, todo_id)
    if not todo or todo.user_id != user_id or todo.deleted_at:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
```

### JWT Token Handling in React

```typescript
// Store access token in memory only (not localStorage)
const [accessToken, setAccessToken] = useState<string | null>(null);

// Refresh token in HttpOnly cookie (set by backend)
// Auto-refresh before expiry using axios interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const newToken = await refreshToken();
      error.config.headers.Authorization = `Bearer ${newToken}`;
      return api.request(error.config);
    }
    return Promise.reject(error);
  }
);
```

---

## Security Considerations

### Rate Limiting Strategy

| Endpoint Type | Limit | Window |
|---------------|-------|--------|
| Auth (login/signup) | 10 requests | 1 minute per IP |
| Token refresh | 30 requests | 1 minute per IP |
| General API | 100 requests | 1 minute per user |

**Implementation**: slowapi library or custom middleware

### CORS Configuration

```python
# Explicit origins, no wildcards in production
origins = settings.CORS_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Required for cookies
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)
```

### Input Validation

| Field | Validation Rules |
|-------|-----------------|
| Email | Valid format, max 255 chars |
| Username | 3-30 chars, alphanumeric + underscore only |
| Password | Min 8 chars, uppercase, lowercase, number |
| Todo title | 1-255 chars, required |
| Tags | Array of strings, each max 50 chars |

---

## Performance Considerations

### Database Indexes

```sql
-- Users table
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Todos table
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_user_status ON todos(user_id, status) WHERE deleted_at IS NULL;
CREATE INDEX idx_todos_user_priority ON todos(user_id, priority) WHERE deleted_at IS NULL;
CREATE INDEX idx_todos_user_created ON todos(user_id, created_at DESC) WHERE deleted_at IS NULL;
```

### Pagination Strategy

- **Method**: Offset-based pagination (simpler for UI)
- **Default page size**: 20 items
- **Maximum page size**: 100 items
- **Response includes**: total count for UI pagination controls

### Frontend Bundle Optimization

- Dynamic imports for route-level code splitting
- Image optimization with next/image
- CSS purging with Tailwind (automatic in production)

---

## Resolved Questions

All technical decisions align with Constitution principles. No NEEDS CLARIFICATION items remain.

| Question | Resolution |
|----------|------------|
| JWT algorithm? | HS256 (simpler for single-service) |
| Password rounds? | 12 (Constitution minimum) |
| Token expiry? | Access: 15min, Refresh: 7 days |
| Pagination style? | Offset-based (simpler UX) |
| State management? | React Context (sufficient for auth) |
| Soft delete retention? | 30 days before permanent deletion |
