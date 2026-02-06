# Full-Stack Todo Application

A production-ready todo application with FastAPI backend and Next.js frontend.

## Features

- User registration and authentication (JWT)
- Todo CRUD operations with user isolation
- Filtering, sorting, and pagination
- Responsive UI with Tailwind CSS
- Dark mode support

## Tech Stack

### Backend
- Python 3.13+
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- PostgreSQL (Neon serverless)
- JWT authentication
- bcrypt password hashing

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Hook Form + Zod
- Axios

## Quick Start

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Setup

#### Backend

```bash
cd backend

# Install dependencies with uv
uv sync

# Copy environment file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local
# Edit .env.local if needed

# Start dev server
npm run dev
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Project Structure

```
fullstack-todo-app/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API routes
│   │   ├── services/        # Business logic
│   │   ├── models/          # SQLModel entities
│   │   ├── db/              # Database setup
│   │   ├── security/        # JWT & password
│   │   └── utils/           # Helpers
│   ├── tests/               # pytest tests
│   └── alembic/             # Migrations
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   ├── services/            # API clients
│   ├── hooks/               # Custom hooks
│   └── types/               # TypeScript types
└── docker-compose.yml
```

## Testing

### Backend

```bash
cd backend
pytest -v --cov=app
```

### Frontend

```bash
cd frontend
npm test
```

## License

MIT
