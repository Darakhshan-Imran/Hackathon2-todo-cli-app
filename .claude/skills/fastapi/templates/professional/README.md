# Professional FastAPI Template

A production-ready FastAPI application structure with authentication, testing, and Docker support.

## Structure

```
app/
├── main.py              # Application entry point
├── config.py            # Configuration management
├── database.py          # Database connection
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── crud/                # Database operations
├── routers/             # API endpoints
├── core/                # Core utilities (auth, security)
└── tests/               # Test files
```

## Setup

1. Install dependencies with uv:
```bash
uv sync
```

2. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Run the application:
```bash
uv run fastapi dev app/main.py
```

## Running Tests

```bash
uv run pytest
```

## Docker

```bash
docker-compose up -d
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
