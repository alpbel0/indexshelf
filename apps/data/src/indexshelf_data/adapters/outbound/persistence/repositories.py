from __future__ import annotations

from typing import Any, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import EventOutboxRecord, JobExecutionRecord


class JobExecutionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_job_id(self, job_id: UUID) -> JobExecutionRecord | None:
        return cast(JobExecutionRecord | None, await self._session.scalar(
            select(JobExecutionRecord).where(JobExecutionRecord.job_id == job_id)
        ))

    async def add(self, job_id: UUID, *, state: str = "received") -> JobExecutionRecord:
        record = JobExecutionRecord(job_id=job_id, state=state)
        self._session.add(record)
        return record


class EventOutboxRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(
        self,
        *,
        event_id: UUID,
        job_id: UUID,
        event_type: str,
        payload: dict[str, Any],
        payload_hash: bytes,
    ) -> EventOutboxRecord:
        record = EventOutboxRecord(
            event_id=event_id,
            job_id=job_id,
            event_type=event_type,
            payload=payload,
            payload_hash=payload_hash,
        )
        self._session.add(record)
        return record

    async def pending(self, limit: int = 100) -> list[EventOutboxRecord]:
        result = await self._session.scalars(
            select(EventOutboxRecord)
            .where(EventOutboxRecord.published_at.is_(None))
            .order_by(EventOutboxRecord.available_at)
            .limit(limit)
            .with_for_update(skip_locked=True)
        )
        return list(result)
