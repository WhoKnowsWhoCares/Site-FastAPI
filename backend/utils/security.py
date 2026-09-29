"""Security utilities: password hashing and JWT token handling."""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
import bcrypt as bcrypt_lib
from pydantic import SecretStr

from backend.config import settings


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt_lib.gensalt()
    hashed = bcrypt_lib.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    pwd_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt_lib.checkpw(pwd_bytes, hashed_bytes)


def create_access_token(
    subject: str,
    email: str,
    is_admin: bool = False,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT access token."""
    expire = (
        datetime.now(timezone.utc) + expires_delta
        if expires_delta
        else datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    )

    to_encode = {
        "sub": subject,
        "email": email,
        "is_admin": is_admin,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    secret = (
        settings.secret_key.get_secret_value()
        if isinstance(settings.secret_key, SecretStr)
        else settings.secret_key
    )

    return jwt.encode(to_encode, secret, algorithm=settings.algorithm)


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token."""
    try:
        secret = (
            settings.secret_key.get_secret_value()
            if isinstance(settings.secret_key, SecretStr)
            else settings.secret_key
        )
        return jwt.decode(token, secret, algorithms=[settings.algorithm])
    except JWTError:
        return None


def get_token_expiry(token: str) -> Optional[datetime]:
    """Get token expiry datetime."""
    payload = decode_token(token)
    if payload and "exp" in payload:
        return datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    return None
