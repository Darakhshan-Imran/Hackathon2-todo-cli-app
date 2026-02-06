"""Health check endpoint."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import text

from app.dependencies import get_db_session

router = APIRouter()


@router.get("")
async def health_check(
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    """
    Health check endpoint.

    Verifies database connectivity and returns service status.
    """
    # Check database connectivity
    try:
        await session.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": db_status,
    }
