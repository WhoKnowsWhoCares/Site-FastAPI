"""Alembic configuration for database migrations."""
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Add project root to path so we can import backend modules
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Import all models so Alembic can detect them (must come after sys.path setup)
from backend.models.base import Base  # noqa: E402

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate
target_metadata = Base.metadata

# Get database URL from settings
from backend.config import settings  # noqa: E402

_migrations_url = settings.database_url
# Alembic migrations run synchronously: use the sync drivers
if _migrations_url.startswith("sqlite+aiosqlite://"):
    _migrations_url = _migrations_url.replace("sqlite+aiosqlite://", "sqlite://", 1)
elif _migrations_url.startswith("postgresql+asyncpg://"):
    _migrations_url = _migrations_url.replace("postgresql+asyncpg://", "postgresql://", 1)
# Override sqlalchemy.url from alembic.ini with the runtime DATABASE_URL
config.set_main_option("sqlalchemy.url", _migrations_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
