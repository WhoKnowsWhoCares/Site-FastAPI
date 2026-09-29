"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""
from typing import Sequence, Union

from alembic import context

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
from sqlalchemy import engine_from_config
from sqlalchemy import pool

# Import all models so Alembic can detect them
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.models.base import Base  # noqa: E402
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = context.config.get_main_option("sqlalchemy.url")
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
        context.config.get_section(context.config.config_ini_section, {}),
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
