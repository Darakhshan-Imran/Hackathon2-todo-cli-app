# Todo App Backend

FastAPI backend for the Full-Stack Todo Application.

## Tech Stack

- **Framework**: FastAPI 0.104+
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL (Neon)
- **Authentication**: JWT (access + refresh tokens)
- **Password Hashing**: bcrypt (12 rounds)
- **Migrations**: Alembic
- **Testing**: pytest + pytest-asyncio

## Project Structure

```
backend/
├── app/
│   ├── api/v1/           # API routes
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── health.py     # Health check
│   │   ├── todos.py      # Todo CRUD endpoints
│   │   ├── users.py      # User profile endpoints
│   │   └── router.py     # Route aggregation
│   ├── db/               # Database configuration
│   │   ├── engine.py     # Async SQLAlchemy engine
│   │   └── base.py       # Session factory
│   ├── middleware/       # Middleware
│   │   └── error_handler.py
│   ├── models/           # SQLModel models
│   │   ├── enums.py      # TodoStatus, Priority
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── todo.py       # Todo model
│   │   └── user.py       # User model
│   ├── security/         # Security utilities
│   │   ├── jwt.py        # JWT token handling
│   │   └── password.py   # Password hashing
│   ├── services/         # Business logic
│   │   ├── auth_service.py
│   │   ├── todo_service.py
│   │   └── user_service.py
│   ├── utils/            # Utilities
│   │   ├── exceptions.py # Custom exceptions
│   │   └── logger.py     # Structured logging
│   ├── config.py         # Settings
│   ├── dependencies.py   # FastAPI dependencies
│   └── main.py           # Application entry
├── alembic/              # Database migrations
├── tests/                # Test suite
│   ├── unit/
│   └── integration/
├── Dockerfile
└── pyproject.toml
```

## Setup

### Prerequisites

- Python 3.13+
- uv (recommended) or pip
- PostgreSQL database

### Installation

```bash
# Install dependencies with uv
uv sync

# Or with pip
pip install -e ".[dev]"
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:pass@host/db` |
| `SECRET_KEY` | JWT signing key (min 32 chars) | `your-secure-random-key` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL | `15` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token TTL | `7` |
| `CORS_ORIGINS` | Allowed origins (comma-separated) | `http://localhost:3000` |

### Database Migrations

```bash
# Run migrations
alembic upgrade head

# Create a new migration
alembic revision --autogenerate -m "description"

# Rollback one migration
alembic downgrade -1
```

### Running the Server

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/health` | Health check | No |
| `POST` | `/api/v1/auth/signup` | Register user | No |
| `POST` | `/api/v1/auth/login` | Login | No |
| `POST` | `/api/v1/auth/refresh` | Refresh tokens | Cookie |
| `POST` | `/api/v1/auth/logout` | Logout | Cookie |
| `GET` | `/api/v1/users/me` | Get profile | Bearer |
| `PATCH` | `/api/v1/users/me` | Update profile | Bearer |
| `GET` | `/api/v1/todos` | List todos | Bearer |
| `POST` | `/api/v1/todos` | Create todo | Bearer |
| `GET` | `/api/v1/todos/{id}` | Get todo | Bearer |
| `PATCH` | `/api/v1/todos/{id}` | Update todo | Bearer |
| `DELETE` | `/api/v1/todos/{id}` | Delete todo | Bearer |

### Response Format

All responses follow this format:

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "timestamp": "2026-02-06T12:00:00Z"
}
```

## Testing

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_auth_service.py -v

# Run integration tests only
pytest tests/integration/ -v
```

## Code Quality

```bash
# Linting
ruff check .

# Fix lint issues
ruff check --fix .

# Type checking
mypy app/

# Format code
ruff format .
```

## Docker

```bash
# Build image
docker build -t todo-backend .

# Run container
docker run -p 8000:8000 --env-file .env todo-backend
```

## Security Features

- **Password Security**: bcrypt with 12 rounds
- **JWT Tokens**: Short-lived access tokens (15 min)
- **Refresh Tokens**: HttpOnly cookies (7 days)
- **User Isolation**: All queries filtered by user_id
- **Input Validation**: Pydantic schemas on all inputs
- **CORS**: Configurable allowed origins

## Architecture Decisions

- **Soft Deletes**: Records have `deleted_at` timestamp instead of hard delete
- **Service Layer**: Business logic separated from API routes
- **Dependency Injection**: FastAPI's DI for database sessions and auth
- **Async/Await**: Full async support for database operations
