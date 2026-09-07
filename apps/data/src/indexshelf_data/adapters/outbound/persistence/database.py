from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class DataBase(DeclarativeBase):
    pass


def create_session_factory(database_url: str) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(database_url, pool_pre_ping=True, pool_recycle=300)
    return async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def transaction(factory: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
    async with factory() as session:
        async with session.begin():
            yield session


def utc_now() -> datetime:
    return datetime.now(UTC)


def uuid7() -> UUID:
    timestamp_ms = int(utc_now().timestamp() * 1000)
    random_bits = UUID(bytes=__import__("secrets").token_bytes(16)).int
    value = (timestamp_ms << 80) | (0x7 << 76) | (random_bits & ((1 << 76) - 1))
    value = (value & ~(0x3 << 62)) | (0x2 << 62)
    return UUID(int=value)
