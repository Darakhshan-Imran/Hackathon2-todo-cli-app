"""Security headers middleware for enhanced protection."""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware that adds security headers to all responses.

    Headers added:
    - X-Content-Type-Options: nosniff - Prevents MIME type sniffing
    - X-Frame-Options: DENY - Prevents clickjacking
    - X-XSS-Protection: 1; mode=block - Legacy XSS filter for older browsers
    - Referrer-Policy: strict-origin-when-cross-origin - Controls referrer info
    - Cache-Control: no-store - Prevents caching of sensitive responses
    - Permissions-Policy: Restricts browser features
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Add security headers to response."""
        response = await call_next(request)

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking - page cannot be embedded in iframes
        response.headers["X-Frame-Options"] = "DENY"

        # Legacy XSS protection for older browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Control how much referrer info is sent
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Prevent caching of API responses (for sensitive data protection)
        # Only for API endpoints, not static files
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store, max-age=0"
            response.headers["Pragma"] = "no-cache"

        # Permissions policy - restrict powerful browser features
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=()"
        )

        return response
