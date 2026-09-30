"""Tests for security utilities."""
from datetime import UTC, timedelta

from backend.utils.security import (
    create_access_token,
    decode_token,
    get_token_expiry,
    hash_password,
    verify_password,
)


def test_hash_and_verify_password():
    """Test password hashing and verification round-trip."""
    password = "my_secure_password_123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)


def test_hash_password_produces_different_hashes():
    """Test that hashing the same password produces different salted hashes."""
    password = "same_password"
    h1 = hash_password(password)
    h2 = hash_password(password)

    assert h1 != h2  # Different salts
    assert verify_password(password, h1)
    assert verify_password(password, h2)


def test_create_and_decode_token():
    """Test creating and decoding a JWT token."""
    token = create_access_token(
        subject="42",
        email="user@example.com",
        is_admin=True,
    )

    assert isinstance(token, str)
    assert len(token) > 0

    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "42"
    assert payload["email"] == "user@example.com"
    assert payload["is_admin"] is True
    assert "exp" in payload
    assert "iat" in payload


def test_create_token_default_expiry():
    """Test token uses default 30-minute expiry."""
    token = create_access_token(
        subject="1",
        email="test@example.com",
    )

    from datetime import datetime
    expiry = get_token_expiry(token)
    assert expiry is not None
    # Default is ~30 minutes from now
    delta = expiry - datetime.now(UTC)
    assert timedelta(minutes=29) < delta < timedelta(minutes=31)


def test_create_token_custom_expiry():
    """Test token with custom expiry duration."""
    token = create_access_token(
        subject="2",
        email="custom@example.com",
        expires_delta=timedelta(hours=1),
    )

    from datetime import datetime
    expiry = get_token_expiry(token)
    delta = expiry - datetime.now(UTC)
    assert timedelta(minutes=59) < delta < timedelta(minutes=61)


def test_decode_invalid_token():
    """Test decoding an invalid token returns None."""
    result = decode_token("not.a.valid.token.here")
    assert result is None


def test_decode_empty_string():
    """Test decoding an empty string returns None."""
    result = decode_token("")
    assert result is None


def test_get_token_expiry_invalid():
    """Test get_token_expiry with invalid token returns None."""
    result = get_token_expiry("invalid.token")
    assert result is None
