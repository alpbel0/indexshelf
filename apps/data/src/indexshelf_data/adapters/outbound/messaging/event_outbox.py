from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from indexshelf_data.adapters.outbound.persistence.models import EventOutboxRecord


async def mark_published(session: AsyncSession, event_id: object) -> None:
    await session.execute(
        update(EventOutboxRecord)
        .where(EventOutboxRecord.event_id == event_id)
        .values(published_at=datetime.now(UTC))
    )
