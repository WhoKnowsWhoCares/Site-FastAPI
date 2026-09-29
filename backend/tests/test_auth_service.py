"""Unit tests for auth_service: JWT create/verify, password hash/verify."""
import time
from datetime import datetime

import pytest
from fastapi import HTTPException

from backend.models.user import User
from backend.services.auth_service import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_and_verify_roundtrip(self):
        hashed = get_password_hash("s3cret-password")
        assert hashed != "s3cret-password"
        assert verify_password("s3cret-password", hashed) is True

    def test_wrong_password_fails_verification(self):
        hashed = get_password_hash("s3cret-password")
        assert verify_password("wrong", hashed) is False

    def test_hashes_are_salted_unique(self):
        assert get_password_hash("same") != get_password_hash("same")


class TestJWTTokens:
    def test_create_token_contains_sub_and_exp(self):
        token = create_access_token({"sub": "42"})
        payload = decode_access_token(token)
        assert payload["sub"] == "42"
        assert "exp" in payload

    def test_default_expiry_is_30_minutes(self):
        now = time.time()
        token = create_access_token({"sub": "42"})
        payload = decode_access_token(token)
        assert 1790 <= payload["exp"] - now <= 1810

    def test_custom_expiry_minutes(self):
        token = create_access_token({"sub": "42"}, expires_minutes=5)
        payload = decode_access_token(token)
        assert 280 <= payload["exp"] - time.time() <= 320

    def test_tampered_token_rejected(self):
        token = create_access_token({"sub": "42"})
        bad = token[:-6] + ("aaaaaa" if token[-6:] != "aaaaaa" else "bbbbbb")
        with pytest.raises(HTTPException) as exc:
            decode_access_token(bad)
        assert exc.value.status_code == 401

    def test_expired_token_rejected(self):
        token = create_access_token({"sub": "42"}, expires_minutes=-1)
        with pytest.raises(HTTPException) as exc:
            decode_access_token(token)
        assert exc.value.status_code == 401

    def test_garbage_token_rejected(self):
        with pytest.raises(HTTPException) as exc:
            decode_access_token("not-a-jwt")
        assert exc.value.status_code == 401

    def test_token_missing_sub_rejected(self):
        token = create_access_token({"foo": "bar"})
        with pytest.raises(HTTPException) as exc:
            decode_access_token(token)
        assert exc.value.status_code == 401
