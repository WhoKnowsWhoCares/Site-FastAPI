"""Tests for models."""
from backend.models.content import ContentType, Media, PageContent, Project, SectionType
from backend.models.user import OAuthAccount, User


def test_user_model_fields():
    """Test User model has all required fields."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_pw",
        is_active=True,
    )
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_pw"
    assert user.is_active is True


def test_user_default_admin():
    """Test User is_admin field defaults to False at DB level."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_pw",
        is_admin=False,
    )
    assert user.is_admin is False


def test_user_repr():
    """Test User __repr__."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_pw",
    )
    repr_str = repr(user)
    assert "User" in repr_str
    assert "test@example.com" in repr_str


def test_oauth_account_model():
    """Test OAuthAccount model."""
    account = OAuthAccount(
        user_id=1,
        provider="github",
        provider_user_id="user123",
    )
    assert account.provider == "github"
    assert account.provider_user_id == "user123"


def test_section_type_enum():
    """Test SectionType enum values."""
    assert SectionType.ABOUTME.value == "aboutme"
    assert SectionType.IHOME.value == "ihome"
    assert SectionType.TRADE4ME.value == "trade4me"
    assert SectionType.SDART.value == "sdart"


def test_content_type_enum():
    """Test ContentType enum values."""
    assert ContentType.HERO.value == "hero"
    assert ContentType.TEXT.value == "text"
    assert ContentType.IMAGE.value == "image"
    assert ContentType.GALLERY.value == "gallery"


def test_page_content_model():
    """Test PageContent model."""
    content = PageContent(
        section=SectionType.ABOUTME,
        content_type=ContentType.TEXT,
        title="About Me",
        body="Hello world",
        order=1,
    )
    assert content.section == SectionType.ABOUTME
    assert content.title == "About Me"


def test_project_model():
    """Test Project model."""
    project = Project(
        section=SectionType.IHOME,
        title="My Home",
        slug="my-home",
        description="Smart home project",
    )
    assert project.section == SectionType.IHOME
    assert project.slug == "my-home"


def test_media_model():
    """Test Media model."""
    media = Media(
        filename="photo.jpg",
        original_filename="photo.jpg",
        content_type="image/jpeg",
        size=1024,
        path="/uploads/photo.jpg",
    )
    assert media.filename == "photo.jpg"
    assert media.content_type == "image/jpeg"
