"""
FastAPI Standard Template
A structured FastAPI application with database integration.

Setup: uv sync
Run with: uv run fastapi dev main.py
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import engine, Base
from routers import items, users

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: Cleanup if needed
    pass

# Initialize FastAPI app
app = FastAPI(
    title="My API",
    description="A standard FastAPI application with database",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(items.router)
app.include_router(users.router)


@app.get("/")
def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to My API!",
        "docs": "/docs",
        "endpoints": {
            "items": "/items",
            "users": "/users"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
