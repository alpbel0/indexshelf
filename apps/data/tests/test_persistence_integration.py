# ruff: noqa: E501
import asyncio
import os
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from indexshelf_data.adapters.outbound.persistence.repositories import (
    EventOutboxRepository,
    JobExecutionRepository,
)
from indexshelf_data.adapters.outbound.persistence.unit_of_work import DataUnitOfWork


def _enabled() -> None:
    if os.getenv("INDEXSHELF_RUN_DATA_DB_SMOKE") != "1":
        pytest.skip("live database smoke is opt-in")


def test_execution_and_outbox_share_transaction() -> None:
    _enabled()

    async def run() -> None:
        url = os.environ["INDEXSHELF_DATA_ASYNC_URL"]
        engine = create_async_engine(url)
        sessions = async_sessionmaker(engine, expire_on_commit=False)
        job_id = uuid4()
        event_id = uuid4()
        uow = DataUnitOfWork(sessions)
        async with uow.transaction() as session:
            await JobExecutionRepository(session).add(job_id)
            await EventOutboxRepository(session).add(
                event_id=event_id,
                job_id=job_id,
                event_type="integration.test",
                payload={"ok": True},
                payload_hash=b"x" * 32,
            )
        async with uow.transaction() as session:
            assert (
                await session.scalar(
                    text("select count(*) from job_execution_records where job_id = :id"),
                    {"id": job_id},
                )
                == 1
            )
            assert (
                await session.scalar(
                    text("select count(*) from event_outbox_records where event_id = :id"),
                    {"id": event_id},
                )
                == 1
            )
            await session.execute(
                text("delete from event_outbox_records where event_id = :id"), {"id": event_id}
            )
            await session.execute(
                text("delete from job_execution_records where job_id = :id"), {"id": job_id}
            )
        failed_job = uuid4()
        failed_event = uuid4()
        with pytest.raises(RuntimeError):
            async with uow.transaction() as session:
                await JobExecutionRepository(session).add(failed_job)
                await EventOutboxRepository(session).add(
                    event_id=failed_event,
                    job_id=failed_job,
                    event_type="integration.rollback",
                    payload={},
                    payload_hash=b"y" * 32,
                )
                raise RuntimeError("rollback")
        async with uow.transaction() as session:
            assert (
                await session.scalar(
                    text("select count(*) from job_execution_records where job_id = :id"),
                    {"id": failed_job},
                )
                == 0
            )
            assert (
                await session.scalar(
                    text("select count(*) from event_outbox_records where event_id = :id"),
                    {"id": failed_event},
                )
                == 0
            )
        await engine.dispose()

    asyncio.run(run())


def test_alembic_can_recreate_data_schema_from_empty_database() -> None:
    _enabled()
    url = os.getenv("INDEXSHELF_DATA_EMPTY_DATABASE_URL")
    if not url:
        pytest.skip("provide INDEXSHELF_DATA_EMPTY_DATABASE_URL for an empty database")
    old_url = os.environ.get("INDEXSHELF_DATA_ALEMBIC_DATABASE_URL")
    os.environ["INDEXSHELF_DATA_ALEMBIC_DATABASE_URL"] = url
    try:
        config = Config(str(Path(__file__).parents[1] / "alembic.ini"))
        command.upgrade(config, "head")
        with psycopg.connect(url.replace("postgresql+psycopg://", "postgresql://")) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select count(*) from information_schema.tables where table_schema = 'public'"
                )
                row = cursor.fetchone()
                assert row is not None and row[0] == 4
    finally:
        if old_url is None:
            os.environ.pop("INDEXSHELF_DATA_ALEMBIC_DATABASE_URL", None)
        else:
            os.environ["INDEXSHELF_DATA_ALEMBIC_DATABASE_URL"] = old_url
