from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import DataBase, uuid7


class JobExecutionRecord(DataBase):
    __tablename__ = "job_execution_records"
    __table_args__ = (
        UniqueConstraint("job_id", name="uq_job_execution_records_job_id"),
        Index("ix_job_execution_records_state_available_at", "state", "available_at"),
    )

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True, default=uuid7)
    job_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False, default="received")
    execution_version: Mapped[int] = mapped_column(BigInteger, nullable=False, default=1)
    lease_token: Mapped[UUID | None] = mapped_column(PgUUID(as_uuid=True))
    lease_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    available_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_error_code: Mapped[str | None] = mapped_column(String(96))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    attempts: Mapped[list[ExtractionAttemptRecord]] = relationship(
        back_populates="execution", cascade="all, delete-orphan"
    )


class ExtractionAttemptRecord(DataBase):
    __tablename__ = "extraction_attempt_records"
    __table_args__ = (
        UniqueConstraint("execution_id", "attempt_number", name="uq_attempt_execution_number"),
        Index("ix_attempt_records_state_created_at", "state", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True, default=uuid7)
    execution_id: Mapped[UUID] = mapped_column(
        ForeignKey("job_execution_records.id", ondelete="CASCADE"), nullable=False
    )
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    strategy: Mapped[str] = mapped_column(String(64), nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False, default="started")
    error_code: Mapped[str | None] = mapped_column(String(96))
    result_ref: Mapped[str | None] = mapped_column(String(512))
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    execution: Mapped[JobExecutionRecord] = relationship(back_populates="attempts")


class EventOutboxRecord(DataBase):
    __tablename__ = "event_outbox_records"
    __table_args__ = (
        UniqueConstraint("event_id", name="uq_event_outbox_records_event_id"),
        Index("ix_event_outbox_records_pending", "published_at", "available_at"),
    )

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True, default=uuid7)
    event_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), nullable=False, default=uuid7)
    job_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), nullable=False)
    event_type: Mapped[str] = mapped_column(String(96), nullable=False)
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    payload_hash: Mapped[bytes] = mapped_column(LargeBinary(32), nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    available_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
