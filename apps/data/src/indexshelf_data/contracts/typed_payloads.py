from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StrictPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CancelReason(StrEnum):
    user_requested = "user_requested"
    superseded = "superseded"
    policy = "policy"


class ComponentName(StrEnum):
    metadata = "metadata"
    static = "static"
    media = "media"
    outbox = "outbox"


class ComponentStatus(StrEnum):
    completed = "completed"
    failed = "failed"
    skipped = "skipped"


class ErrorCode(StrEnum):
    invalid_url = "INVALID_URL"
    unsupported_scheme = "UNSUPPORTED_SCHEME"
    connect_timeout = "CONNECT_TIMEOUT"
    read_timeout = "READ_TIMEOUT"
    http_access_denied = "HTTP_ACCESS_DENIED"
    http_not_found = "HTTP_NOT_FOUND"
    http_rate_limited = "HTTP_RATE_LIMITED"
    http_server_error = "HTTP_SERVER_ERROR"
    content_extraction_empty = "CONTENT_EXTRACTION_EMPTY"
    content_validation_failed = "CONTENT_VALIDATION_FAILED"
    unsupported_mime = "UNSUPPORTED_MIME"
    captcha_required = "CAPTCHA_REQUIRED"
    robots_policy_denied = "ROBOTS_POLICY_DENIED"
    proxy_unavailable = "PROXY_UNAVAILABLE"
    proxy_configuration_error = "PROXY_CONFIGURATION_ERROR"
    dependency_unavailable = "DEPENDENCY_UNAVAILABLE"
    browser_operation_timeout = "BROWSER_OPERATION_TIMEOUT"
    browser_crashed = "BROWSER_CRASHED"
    worker_interrupted = "WORKER_INTERRUPTED"
    cancelled = "CANCELLED"


class ContentRef(StrictPayload):
    ref: str = Field(pattern=r"^[a-zA-Z0-9][a-zA-Z0-9._/-]{0,511}$")
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    content_type: str = Field(pattern=r"^[a-z0-9!#$&^_.+-]+/[a-z0-9!#$&^_.+-]+$", max_length=127)
    size_bytes: int = Field(ge=0, le=52_428_800)
    expires_at: datetime


class StableError(StrictPayload):
    error_code: ErrorCode
    retryable: bool
    message: str = Field(min_length=1, max_length=500)
    stage: Literal["fetch", "browser", "extract", "validate", "media", "publish"] | None = None
    details_ref: ContentRef | None = None


class CancelJobPayload(StrictPayload):
    job_id: UUID
    reason: CancelReason


class JobCancelledPayload(StrictPayload):
    job_id: UUID
    reason: CancelReason
    cancelled_at: datetime


class ComponentResult(StrictPayload):
    name: ComponentName
    status: ComponentStatus
    content_ref: ContentRef | None = None


class JobCompletedPayload(StrictPayload):
    job_id: UUID
    partial: bool
    components: Annotated[list[ComponentResult], Field(min_length=1)]


class JobFailedPayload(StrictPayload):
    job_id: UUID
    error: StableError


class ComponentFailedPayload(StrictPayload):
    job_id: UUID
    component: ComponentName
    error: StableError


TypedPayload = (
    CancelJobPayload
    | JobCompletedPayload
    | JobFailedPayload
    | JobCancelledPayload
    | ComponentFailedPayload
)


PAYLOAD_MODELS: dict[str, type[StrictPayload]] = {
    "job.cancel": CancelJobPayload,
    "job.completed": JobCompletedPayload,
    "job.failed": JobFailedPayload,
    "job.cancelled": JobCancelledPayload,
    "component.failed": ComponentFailedPayload,
}
