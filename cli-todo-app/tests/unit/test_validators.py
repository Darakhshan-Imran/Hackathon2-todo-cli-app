"""Unit tests for validators - validate_title, validate_id, validate_status_filter."""

import pytest

from src.exceptions import EmptyTitleError, InvalidIdError
from src.utils import validate_id, validate_status_filter, validate_title


class TestValidateTitle:
    """Tests for validate_title function."""

    def test_valid_title(self) -> None:
        """Valid title is returned as-is."""
        assert validate_title("Buy groceries") == "Buy groceries"

    def test_title_with_leading_whitespace(self) -> None:
        """Leading whitespace is stripped."""
        assert validate_title("  Buy groceries") == "Buy groceries"

    def test_title_with_trailing_whitespace(self) -> None:
        """Trailing whitespace is stripped."""
        assert validate_title("Buy groceries  ") == "Buy groceries"

    def test_title_with_surrounding_whitespace(self) -> None:
        """Surrounding whitespace is stripped."""
        assert validate_title("  Buy groceries  ") == "Buy groceries"

    def test_empty_title_raises_error(self) -> None:
        """Empty string raises EmptyTitleError."""
        with pytest.raises(EmptyTitleError):
            validate_title("")

    def test_whitespace_only_title_raises_error(self) -> None:
        """Whitespace-only string raises EmptyTitleError."""
        with pytest.raises(EmptyTitleError):
            validate_title("   ")

    def test_title_with_internal_spaces(self) -> None:
        """Internal spaces are preserved."""
        assert validate_title("Buy some groceries") == "Buy some groceries"


class TestValidateId:
    """Tests for validate_id function."""

    def test_valid_integer_id(self) -> None:
        """Valid integer ID is returned."""
        assert validate_id(1) == 1
        assert validate_id(42) == 42
        assert validate_id(100) == 100

    def test_valid_string_id(self) -> None:
        """Valid string ID is parsed and returned."""
        assert validate_id("1") == 1
        assert validate_id("42") == 42
        assert validate_id("100") == 100

    def test_zero_id_raises_error(self) -> None:
        """Zero ID raises InvalidIdError."""
        with pytest.raises(InvalidIdError):
            validate_id(0)

    def test_negative_id_raises_error(self) -> None:
        """Negative ID raises InvalidIdError."""
        with pytest.raises(InvalidIdError):
            validate_id(-1)

    def test_non_numeric_string_raises_error(self) -> None:
        """Non-numeric string raises InvalidIdError."""
        with pytest.raises(InvalidIdError):
            validate_id("abc")

    def test_float_string_raises_error(self) -> None:
        """Float string raises InvalidIdError."""
        with pytest.raises(InvalidIdError):
            validate_id("1.5")

    def test_empty_string_raises_error(self) -> None:
        """Empty string raises InvalidIdError."""
        with pytest.raises(InvalidIdError):
            validate_id("")


class TestValidateStatusFilter:
    """Tests for validate_status_filter function."""

    def test_none_returns_none(self) -> None:
        """None input returns None."""
        assert validate_status_filter(None) is None

    def test_complete_lowercase(self) -> None:
        """'complete' is valid and returned lowercase."""
        assert validate_status_filter("complete") == "complete"

    def test_incomplete_lowercase(self) -> None:
        """'incomplete' is valid and returned lowercase."""
        assert validate_status_filter("incomplete") == "incomplete"

    def test_complete_uppercase(self) -> None:
        """'COMPLETE' is valid and returned lowercase."""
        assert validate_status_filter("COMPLETE") == "complete"

    def test_incomplete_uppercase(self) -> None:
        """'INCOMPLETE' is valid and returned lowercase."""
        assert validate_status_filter("INCOMPLETE") == "incomplete"

    def test_mixed_case(self) -> None:
        """Mixed case is valid and returned lowercase."""
        assert validate_status_filter("Complete") == "complete"
        assert validate_status_filter("InComplete") == "incomplete"

    def test_invalid_status_raises_error(self) -> None:
        """Invalid status raises ValueError."""
        with pytest.raises(ValueError):
            validate_status_filter("pending")

    def test_empty_string_raises_error(self) -> None:
        """Empty string raises ValueError."""
        with pytest.raises(ValueError):
            validate_status_filter("")
