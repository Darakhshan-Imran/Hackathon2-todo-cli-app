"""Global exception handlers for consistent error responses."""

from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError

from app.utils.exceptions import AppException


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers with the FastAPI app."""

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request, exc: AppException
    ) -> JSONResponse:
        """Handle application-specific exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "data": None,
                "error": exc.message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    @app.exception_handler(PydanticValidationError)
    async def validation_exception_handler(
        request: Request, exc: PydanticValidationError
    ) -> JSONResponse:
        """Handle Pydantic validation errors."""
        # Extract first error message for user-friendly response
        errors = exc.errors()
        if errors:
            first_error = errors[0]
            field = ".".join(str(loc) for loc in first_error.get("loc", []))
            message = f"Validation error: {field} - {first_error.get('msg', 'invalid')}"
        else:
            message = "Validation error"

        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "data": None,
                "error": message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle unexpected exceptions - don't leak sensitive details."""
        # Log the actual error for debugging (but not in response)
        from app.utils.logger import logger

        logger.exception("Unexpected error occurred")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "data": None,
                "error": "An unexpected error occurred",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )
