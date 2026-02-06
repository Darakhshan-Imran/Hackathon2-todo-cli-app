"""Structured logging configuration."""

import logging
import sys
from typing import Any

from app.config import get_settings


class StructuredFormatter(logging.Formatter):
    """JSON-like structured log formatter for production."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured output."""
        settings = get_settings()

        if settings.is_production:
            # JSON format for production
            import json
            from datetime import datetime, timezone

            log_data: dict[str, Any] = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }

            if record.exc_info:
                log_data["exception"] = self.formatException(record.exc_info)

            # Add extra fields
            for key, value in record.__dict__.items():
                if key not in {
                    "name",
                    "msg",
                    "args",
                    "created",
                    "filename",
                    "funcName",
                    "levelname",
                    "levelno",
                    "lineno",
                    "module",
                    "msecs",
                    "pathname",
                    "process",
                    "processName",
                    "relativeCreated",
                    "stack_info",
                    "thread",
                    "threadName",
                    "exc_info",
                    "exc_text",
                    "message",
                }:
                    log_data[key] = value

            return json.dumps(log_data)

        # Human-readable format for development
        return super().format(record)


def setup_logging() -> logging.Logger:
    """Configure application logging."""
    settings = get_settings()

    # Create logger
    logger = logging.getLogger("app")
    logger.setLevel(getattr(logging, settings.log_level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    # Set formatter
    if settings.is_production:
        formatter = StructuredFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Create default logger instance
logger = setup_logging()


def log_security_event(
    event_type: str,
    user_id: str | None = None,
    ip_address: str | None = None,
    success: bool = True,
    details: str | None = None,
) -> None:
    """
    Log security-related events.

    Args:
        event_type: Type of event (login, logout, signup, failed_auth)
        user_id: User ID if known (never log sensitive details)
        ip_address: Client IP address
        success: Whether the operation succeeded
        details: Additional non-sensitive details
    """
    extra = {
        "event_type": event_type,
        "success": success,
    }

    if user_id:
        extra["user_id"] = user_id
    if ip_address:
        extra["ip_address"] = ip_address
    if details:
        extra["details"] = details

    level = logging.INFO if success else logging.WARNING
    logger.log(level, f"Security event: {event_type}", extra=extra)
