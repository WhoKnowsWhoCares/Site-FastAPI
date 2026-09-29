"""Tests for authentication service."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.user import User, OAuthAccount
from backend.schemas.auth import UserCreate
from backend.services.auth_service import AuthService
from backend.utils.security import hash_password, verify_password


@pytest.fixture
async def auth_service(test_db: AsyncSession) -> AuthService:
    return AuthService(test_db)


@pytest.mark.asyncio
async def test_hash_password(auth_service: AuthService):
    """Test password hashing."""
    plain = "securepassword123"
    hashed = hash_password(plain)

    assert hashed != plain
    assert verify_password(plain, hashed)
    assert not verify_password("wrongpassword", hashed)


@pytest.mark.asyncio
async def test_create_user(auth_service: AuthService):
    """Test user creation."""
    user_data = UserCreate(
        email="newuser@example.com",
        name="New User",
        password="securepassword123",
    )

    user = await auth_service.create_user(user_data)

    assert user.id is not None
    assert user.email == "newuser@example.com"
    assert user.name == "New User"
    assert user.hashed_password is not None
    assert verify_password("securepassword123", user.hashed_password)


@pytest.mark.asyncio
async def test_get_user_by_email(auth_service: AuthService):
    """Test getting user by email."""
    # Create a user first
    user = await auth_service.create_user(
        UserCreate(email="findme@example.com", name="Find Me", password="password123")
    )

    # Find the user
    found = await auth_service.get_user_by_email("findme@example.com")
    assert found is not None
    assert found.id == user.id
    assert found.email == "findme@example.com"


@pytest.mark.asyncio
async def test_get_user_not_found(auth_service: AuthService):
    """Test getting non-existent user."""
    found = await auth_service.get_user_by_email("nonexistent@example.com")
    assert found is None


@pytest.mark.asyncio
async def test_authenticate_success(auth_service: AuthService):
    """Test successful authentication."""
    # Create a user
    await auth_service.create_user(
        UserCreate(email="authuser@example.com", name="Auth User", password="password123")
    )

    # Authenticate
    authenticated = await auth_service.authenticate("authuser@example.com", "password123")
    assert authenticated is not None
    assert authenticated.email == "authuser@example.com"


@pytest.mark.asyncio
async def test_authenticate_wrong_password(auth_service: AuthService):
    """Test authentication with wrong password."""
    # Create a user
    await auth_service.create_user(
        UserCreate(email="authuser2@example.com", name="Auth User 2", password="password123")
    )

    # Try to authenticate with wrong password
    authenticated = await auth_service.authenticate("authuser2@example.com", "wrongpassword")
    assert authenticated is None


@pytest.mark.asyncio
async def test_authenticate_nonexistent_user(auth_service: AuthService):
    """Test authentication with non-existent user."""
    authenticated = await auth_service.authenticate("nonexistent@example.com", "password123")
    assert authenticated is None


@pytest.mark.asyncio
async def test_create_token(auth_service: AuthService):
    """Test token creation."""
    # Create a user
    user = await auth_service.create_user(
        UserCreate(email="tokenuser@example.com", name="Token User", password="password123")
    )

    # Create token
    token = auth_service.create_token(user)
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.asyncio
async def test_decode_token(auth_service: AuthService):
    """Test token decoding."""
    # Create a user
    user = await auth_service.create_user(
        UserCreate(email="decodeuser@example.com", name="Decode User", password="password123")
    )

    # Create and decode token
    token = auth_service.create_token(user)
    token_data = auth_service.decode_token(token)

    assert token_data is not None
    assert token_data.sub == str(user.id)
    assert token_data.email == "decodeuser@example.com"


@pytest.mark.asyncio
async def test_decode_invalid_token(auth_service: AuthService):
    """Test decoding invalid token."""
    token_data = auth_service.decode_token("invalid.token.here")
    assert token_data is None


@pytest.mark.asyncio
async def test_oauth_user_creation(auth_service: AuthService):
    """Test creating user from OAuth."""
    user = await auth_service.create_oauth_user(
        email="oauth@example.com",
        name="OAuth User",
        avatar_url="https://example.com/avatar.png",
        provider="github",
        provider_user_id="github123456",
        access_token="fake_access_token",
    )

    assert user.id is not None
    assert user.email == "oauth@example.com"
    assert user.hashed_password is None  # OAuth users don't have passwords initially


@pytest.mark.asyncio
async def test_oauth_user_find(auth_service: AuthService):
    """Test finding user by OAuth account."""
    # Create OAuth user
    await auth_service.create_oauth_user(
        email="findoauth@example.com",
        name="Find OAuth User",
        avatar_url=None,
        provider="google",
        provider_user_id="google789012",
    )

    # Find the user
    found = await auth_service.get_user_by_oauth("google", "google789012")
    assert found is not None
    assert found.email == "findoauth@example.com"


@pytest.mark.asyncio
async def test_update_user(auth_service: AuthService):
    """Test updating user."""
    # Create a user
    user = await auth_service.create_user(
        UserCreate(email="updateuser@example.com", name="Original Name", password="password123")
    )

    # Update user
    from backend.schemas.auth import UserUpdate
    updated = await auth_service.update_user(
        user,
        UserUpdate(name="Updated Name", avatar_url="https://example.com/new-avatar.png"),
    )

    assert updated.name == "Updated Name"
    assert updated.avatar_url == "https://example.com/new-avatar.png"


@pytest.mark.asyncio
async def test_set_password(auth_service: AuthService):
    """Test setting password for OAuth user."""
    # Create OAuth user without password
    user = await auth_service.create_oauth_user(
        email="setpass@example.com",
        name="Set Password User",
        provider="github",
        provider_user_id="github999",
    )

    assert user.hashed_password is None

    # Set password
    updated = await auth_service.set_password(user, "newpassword456")
    assert updated.hashed_password is not None
    assert verify_password("newpassword456", updated.hashed_password)
