"""Custom exceptions for Todo CLI."""


class TodoError(Exception):
    """Base exception for all todo-related errors."""

    def __init__(self, message: str, code: str = "TODO_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)


class TodoNotFoundError(TodoError):
    """Raised when a todo with the specified ID is not found."""

    def __init__(self, todo_id: int) -> None:
        self.todo_id = todo_id
        super().__init__(
            message=f"Todo with ID {todo_id} not found",
            code="TODO_NOT_FOUND",
        )


class ValidationError(TodoError):
    """Raised when input validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="VALIDATION_ERROR")


class EmptyTitleError(ValidationError):
    """Raised when todo title is empty."""

    def __init__(self) -> None:
        super().__init__(message="Title is required")


class InvalidIdError(ValidationError):
    """Raised when ID is not a valid positive integer."""

    def __init__(self) -> None:
        super().__init__(message="Invalid ID. ID must be a positive number")


class CommandError(TodoError):
    """Raised when a command is unknown or malformed."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="COMMAND_ERROR")
