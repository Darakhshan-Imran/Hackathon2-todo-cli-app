# Quickstart: Full-Stack Todo Application

**Feature**: `1-fullstack-todo-app`
**Date**: 2026-02-05

This guide gets you up and running with the Full-Stack Todo Application for local development.

## Prerequisites

- **Python 3.13+** with `uv` package manager
- **Node.js 20+** with npm
- **PostgreSQL** (or Neon account for serverless)
- **Git**

## Quick Setup (5 minutes)

### 1. Clone and Navigate

```bash
cd fullstack-todo-app
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Copy environment file and configure
cp .env.example .env
# Edit .env with your database URL and JWT secret
```

**Required environment variables** in `backend/.env`:

```bash
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/todo_db
JWT_SECRET_KEY=your-super-secret-key-at-least-32-characters-long
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

### 3. Database Setup

```bash
# Create database (if using local PostgreSQL)
createdb todo_db

# Run migrations
alembic upgrade head
```

### 4. Start Backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend running at: http://localhost:8000
API docs at: http://localhost:8000/docs

### 5. Frontend Setup (new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local
```

**Required environment variables** in `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=Todo App
```

### 6. Start Frontend

```bash
npm run dev
```

Frontend running at: http://localhost:3000

---

## Development Workflow

### Running Tests

**Backend:**
```bash
cd backend
pytest                    # All tests
pytest tests/unit        # Unit tests only
pytest tests/integration # Integration tests only
pytest --cov=app        # With coverage
```

**Frontend:**
```bash
cd frontend
npm test                 # Unit tests
npm run test:e2e        # E2E tests (Playwright)
```

### Code Quality

**Backend:**
```bash
ruff check .            # Linting
ruff format .           # Formatting
mypy app               # Type checking
```

**Frontend:**
```bash
npm run lint           # ESLint
npm run type-check     # TypeScript
```

### Database Migrations

```bash
cd backend

# Create new migration after model changes
alembic revision --autogenerate -m "description of change"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

---

## Docker Development

For a complete local environment with Docker:

```bash
# From project root
docker-compose up -d

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# Database: localhost:5432
```

### docker-compose.yml structure:

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    env_file:
      - ./frontend/.env.local

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: todo
      POSTGRES_PASSWORD: todo
      POSTGRES_DB: todo_db
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  pgdata:
```

---

## API Endpoints Quick Reference

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/signup` | Register new user | No |
| POST | `/api/v1/auth/login` | Login | No |
| POST | `/api/v1/auth/refresh` | Refresh token | Cookie |
| POST | `/api/v1/auth/logout` | Logout | Yes |
| GET | `/api/v1/todos` | List todos | Yes |
| POST | `/api/v1/todos` | Create todo | Yes |
| GET | `/api/v1/todos/{id}` | Get todo | Yes |
| PATCH | `/api/v1/todos/{id}` | Update todo | Yes |
| DELETE | `/api/v1/todos/{id}` | Delete todo | Yes |
| GET | `/api/v1/users/me` | Get profile | Yes |
| PATCH | `/api/v1/users/me` | Update profile | Yes |
| GET | `/api/v1/health` | Health check | No |

---

## Testing the API

### Using curl:

```bash
# 1. Register
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"Password123"}'

# 2. Login (save the token)
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Password123"}' \
  | jq -r '.data.access_token')

# 3. Create todo
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"My first todo","priority":"high"}'

# 4. List todos
curl http://localhost:8000/api/v1/todos \
  -H "Authorization: Bearer $TOKEN"
```

### Using the Swagger UI:

1. Open http://localhost:8000/docs
2. Use "Try it out" button on endpoints
3. For authenticated endpoints, click "Authorize" and paste your JWT

---

## Troubleshooting

### Common Issues

**Database connection failed:**
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Verify database exists: `psql -l`

**JWT errors:**
- Ensure JWT_SECRET_KEY is at least 32 characters
- Check token hasn't expired (15 min for access)

**CORS errors:**
- Verify CORS_ORIGINS includes frontend URL
- Check no trailing slash in URLs

**Port already in use:**
```bash
# Find process using port 8000
lsof -i :8000
# Kill it
kill -9 <PID>
```

### Logs

**Backend logs:**
```bash
# With uvicorn
uvicorn app.main:app --reload --log-level debug
```

**Frontend logs:**
- Check browser console
- Check terminal running `npm run dev`

---

## Next Steps

1. Review the [API documentation](http://localhost:8000/docs)
2. Check the [OpenAPI spec](./contracts/openapi.yaml)
3. Read the [Implementation Plan](./plan.md)
4. Start with Sprint 1 tasks in [tasks.md](./tasks.md)

---

## Useful Commands Cheatsheet

```bash
# Backend
cd backend && source .venv/bin/activate
uvicorn app.main:app --reload              # Start server
pytest -v                                   # Run tests
alembic upgrade head                        # Apply migrations

# Frontend
cd frontend
npm run dev                                 # Start dev server
npm run build                               # Production build
npm run lint                                # Check code style

# Docker
docker-compose up -d                        # Start all services
docker-compose logs -f backend              # Follow backend logs
docker-compose down                         # Stop all services
```
