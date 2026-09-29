"""Tests for backend config."""
from backend.config import settings


def test_settings_database_url():
    """Test that settings.database_url is accessible and has default value."""
    assert hasattr(settings, "database_url")
    assert settings.database_url == "sqlite:///./site.db"


def test_settings_secret_key():
    """Test that secret_key is accessible."""
    assert hasattr(settings, "secret_key")
    assert isinstance(settings.secret_key, str)
    assert len(settings.secret_key) > 0


def test_settings_debug():
    """Test debug setting."""
    assert hasattr(settings, "debug")
    assert isinstance(settings.debug, bool)


def test_settings_all_required_fields():
    """Test that all required settings fields exist."""
    assert hasattr(settings, "app_name")
    assert hasattr(settings, "version")
    assert hasattr(settings, "algorithm")
    assert hasattr(settings, "access_token_expire_minutes")
    assert hasattr(settings, "host")
    assert hasattr(settings, "port")
    assert hasattr(settings, "frontend_url")
