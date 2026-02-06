"""API v1 router - combines all v1 routes."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.todos import router as todos_router
from app.api.v1.users import router as users_router

api_router = APIRouter()

# Include all route modules
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(todos_router, prefix="/todos", tags=["todos"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
