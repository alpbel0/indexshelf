from __future__ import annotations

from alembic import context
from sqlalchemy import engine_from_config, pool

from indexshelf_data.adapters.outbound.persistence import models  # noqa: F401
from indexshelf_data.adapters.outbound.persistence.database import DataBase
from indexshelf_data.bootstrap.settings import DataSettings

config = context.config
target_metadata = DataBase.metadata


def database_url() -> str:
    url = DataSettings().alembic_database_url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


def run_migrations_offline() -> None:
    context.configure(
        url=database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    section = config.get_section(config.config_ini_section) or {}
    section["sqlalchemy.url"] = database_url()
    connectable = engine_from_config(section, prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
