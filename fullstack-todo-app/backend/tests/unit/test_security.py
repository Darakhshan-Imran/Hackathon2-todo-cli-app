"""Unit tests for security functions."""

from uuid import uuid4

import pytest

from app.security.jwt import (
    TokenError,
    create_access_token,
    create_refresh_token,
    get_user_id_from_token,
    verify_token,
)
from app.security.password import hash_password, verify_password


class TestPasswordSecurity:
    """Tests for password hashing."""

    def test_hash_password_creates_hash(self):
        """Hash password should create a bcrypt hash."""
        password = "TestPassword123"
        hashed = hash_password(password)

        # Bcrypt hashes start with $2b$
        assert hashed.startswith("$2b$")
        assert hashed != password

    def test_hash_password_different_hashes(self):
        """Same password should create different hashes (due to salt)."""
        password = "TestPassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2

    def test_verify_password_correct(self):
        """Verify should return True for correct password."""
        password = "TestPassword123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Verify should return False for incorrect password."""
        password = "TestPassword123"
        hashed = hash_password(password)

        assert verify_password("WrongPassword", hashed) is False

    def test_verify_password_case_sensitive(self):
        """Password verification should be case-sensitive."""
        password = "TestPassword123"
        hashed = hash_password(password)

        assert verify_password("testpassword123", hashed) is False
        assert verify_password("TESTPASSWORD123", hashed) is False


class TestJWTSecurity:
    """Tests for JWT token functions."""

    def test_create_access_token(self):
        """Create access token should return valid JWT."""
        user_id = uuid4()
        token = create_access_token(user_id)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token(self):
        """Create refresh token should return valid JWT."""
        user_id = uuid4()
        token = create_refresh_token(user_id)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_access_token(self):
        """Verify should decode valid access token."""
        user_id = uuid4()
        token = create_access_token(user_id)

        payload = verify_token(token, token_type="access")

        assert payload["sub"] == str(user_id)
        assert payload["type"] == "access"

    def test_verify_refresh_token(self):
        """Verify should decode valid refresh token."""
        user_id = uuid4()
        token = create_refresh_token(user_id)

        payload = verify_token(token, token_type="refresh")

        assert payload["sub"] == str(user_id)
        assert payload["type"] == "refresh"
        assert "jti" in payload  # Unique token ID for rotation

    def test_verify_token_wrong_type(self):
        """Verify should reject token with wrong type."""
        user_id = uuid4()
        access_token = create_access_token(user_id)

        with pytest.raises(TokenError, match="Invalid token type"):
            verify_token(access_token, token_type="refresh")

    def test_verify_invalid_token(self):
        """Verify should reject invalid token."""
        with pytest.raises(TokenError, match="Invalid token"):
            verify_token("invalid-token", token_type="access")

    def test_get_user_id_from_token(self):
        """Get user ID should extract UUID from token."""
        user_id = uuid4()
        token = create_access_token(user_id)

        extracted_id = get_user_id_from_token(token)

        assert extracted_id == user_id

    def test_tokens_are_different(self):
        """Access and refresh tokens should be different."""
        user_id = uuid4()
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)

        assert access_token != refresh_token
