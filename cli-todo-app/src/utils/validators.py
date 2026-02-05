"""Input validators for Todo CLI."""

from src.exceptions import EmptyTitleError, InvalidIdError


def validate_title(title: str) -> str:
    """Validate and clean a todo title.

    Args:
        title: The title to validate

    Returns:
        The cleaned title (stripped of leading/trailing whitespace)

    Raises:
        EmptyTitleError: If title is empty or only whitespace
    """
    cleaned = title.strip()
    if not cleaned:
        raise EmptyTitleError()
    return cleaned


def validate_id(value: str | int) -> int:
    """Validate and parse a todo ID.

    Args:
        value: The ID value to validate (string or int)

    Returns:
        The validated ID as an integer

    Raises:
        InvalidIdError: If ID is not a positive integer
    """
    try:
        id_int = int(value)
        if id_int <= 0:
            raise InvalidIdError()
        return id_int
    except (ValueError, TypeError):
        raise InvalidIdError()


def validate_status_filter(status: str | None) -> str | None:
    """Validate a status filter value.

    Args:
        status: The status filter value (complete, incomplete, or None)

    Returns:
        The validated status string or None

    Raises:
        ValueError: If status is not a valid value
    """
    if status is None:
        return None
    valid_statuses = {"complete", "incomplete"}
    if status.lower() not in valid_statuses:
        raise ValueError("Invalid status. Use 'complete' or 'incomplete'")
    return status.lower()
