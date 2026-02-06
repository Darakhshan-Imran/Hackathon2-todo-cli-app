"""FastAPI application entry point with lifespan management."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config import get_settings
from app.db.engine import dispose_engine, init_engine
from app.middleware.error_handler import register_exception_handlers
from app.middleware.security_headers import SecurityHeadersMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifespan - startup and shutdown events."""
    # Startup
    settings = get_settings()
    await init_engine(settings.database_url)
    yield
    # Shutdown
    await dispose_engine()


def create_app() -> FastAPI:
    """Application factory - creates and configures FastAPI app."""
    settings = get_settings()

    app = FastAPI(
        title="Full-Stack Todo API",
        description="RESTful API for the Full-Stack Todo Application with JWT authentication",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/api/docs" if not settings.is_production else None,
        redoc_url="/api/redoc" if not settings.is_production else None,
    )

    # Security headers middleware (added first, runs last)
    app.add_middleware(SecurityHeadersMiddleware)

    # CORS middleware - explicit origins only
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    # Register exception handlers
    register_exception_handlers(app)

    # Include API router
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/")
    async def root() -> dict[str, str]:
        """Root endpoint."""
        return {"message": "Full-Stack Todo API", "docs": "/api/docs"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
