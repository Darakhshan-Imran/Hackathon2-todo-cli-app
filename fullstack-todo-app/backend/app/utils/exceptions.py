"""Custom exception classes."""


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class AuthenticationError(AppException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, status_code=401)


class AuthorizationError(AppException):
    """Raised when user lacks permission."""

    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, status_code=403)


class NotFoundError(AppException):
    """Raised when resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ConflictError(AppException):
    """Raised when there's a conflict (e.g., duplicate resource)."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409)


class ValidationError(AppException):
    """Raised when validation fails."""

    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=400)
