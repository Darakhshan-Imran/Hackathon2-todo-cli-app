# Deploying FastAPI Applications

Production deployment with Docker, Gunicorn, and cloud platforms.

---

## Production Server

### Uvicorn (ASGI Server)
```bash
# Development
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Gunicorn with Uvicorn Workers
```bash
uv add gunicorn

# Run with multiple workers
uv run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Calculate Workers
```python
# Rule of thumb: (2 x CPU cores) + 1
import multiprocessing
workers = (2 * multiprocessing.cpu_count()) + 1
```

---

## Docker Deployment

### Basic Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application
COPY . .

# Run
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Optimized Dockerfile
```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Create non-root user
RUN useradd --create-home appuser
USER appuser

# Copy application
COPY --chown=appuser:appuser . .

EXPOSE 8000
CMD ["uv", "run", "gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
```

---

## Environment Configuration

### .env File
```bash
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
SECRET_KEY=your-super-secret-key-here
DEBUG=false
ALLOWED_HOSTS=example.com,www.example.com
```

### Load Environment Variables
```python
# config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False
    allowed_hosts: list[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
```

### Use in Application
```python
from config import settings

app = FastAPI(debug=settings.debug)

DATABASE_URL = settings.database_url
SECRET_KEY = settings.secret_key
```

---

## Nginx Reverse Proxy

### nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    upstream fastapi {
        server api:8000;
    }

    server {
        listen 80;
        server_name example.com;

        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name example.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://fastapi;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static {
            alias /app/static;
        }
    }
}
```

---

## Cloud Deployments

### Railway
```bash
# Install CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**railway.json**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT"
  }
}
```

### Render
**render.yaml**
```yaml
services:
  - type: web
    name: fastapi-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: mydb
          property: connectionString
```

### AWS (Elastic Beanstalk)
```bash
# Install EB CLI
uv tool install awsebcli

# Initialize
eb init -p python-3.11 my-fastapi-app

# Create environment
eb create production
```

**Procfile**
```
web: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Google Cloud Run
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/fastapi-app

# Deploy
gcloud run deploy fastapi-app \
  --image gcr.io/PROJECT_ID/fastapi-app \
  --platform managed \
  --allow-unauthenticated
```

---

## Health Checks

### Basic Health Check
```python
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### Comprehensive Health Check
```python
from sqlalchemy import text

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    health = {"status": "healthy", "checks": {}}

    # Database check
    try:
        db.execute(text("SELECT 1"))
        health["checks"]["database"] = "ok"
    except Exception as e:
        health["status"] = "unhealthy"
        health["checks"]["database"] = str(e)

    # Redis check (if using)
    # try:
    #     await redis.ping()
    #     health["checks"]["redis"] = "ok"
    # except Exception as e:
    #     health["status"] = "unhealthy"
    #     health["checks"]["redis"] = str(e)

    status_code = 200 if health["status"] == "healthy" else 503
    return JSONResponse(content=health, status_code=status_code)
```

---

## Logging

### Configure Logging
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            "app.log",
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
    ]
)

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
```

### JSON Logging (Production)
```python
import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.getLogger().addHandler(handler)
```

---

## Security Checklist

### Production Checklist
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(
    title="My API",
    docs_url=None if not settings.debug else "/docs",  # Disable in production
    redoc_url=None if not settings.debug else "/redoc",
    openapi_url=None if not settings.debug else "/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

---

## pyproject.toml (Production)
```toml
[project]
name = "my-fastapi-app"
version = "1.0.0"
description = "Production FastAPI application"
requires-python = ">=3.11"
dependencies = [
    "fastapi[standard]>=0.109.0",
    "gunicorn>=21.2.0",
    "sqlalchemy>=2.0.25",
    "psycopg2-binary>=2.9.9",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.6",
    "pydantic-settings>=2.1.0",
]

[dependency-groups]
dev = [
    "pytest>=7.4.0",
    "httpx>=0.26.0",
    "pytest-asyncio>=0.23.0",
]
```

---

## Complete Production Setup

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── crud/
│   └── routers/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
└── README.md
```
