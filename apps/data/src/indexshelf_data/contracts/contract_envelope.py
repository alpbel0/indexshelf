from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .typed_payloads import PAYLOAD_MODELS, StrictPayload


class InvalidContractError(ValueError):
    pass


class Subject(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    kind: str
    id: UUID


class ContractEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow", strict=True)
    message_id: UUID
    message_kind: str
    message_type: str
    message_version: int = Field(strict=True)
    occurred_at: datetime
    correlation_id: UUID
    causation_id: UUID | None = None
    producer: str
    subject: Subject
    payload: dict[str, object]

    @field_validator("message_kind")
    @classmethod
    def validate_kind(cls, value: str) -> str:
        if value not in {"command", "event"}:
            raise InvalidContractError("unsupported message kind")
        return value

    @field_validator("message_version")
    @classmethod
    def validate_version(cls, value: int) -> int:
        if value != 1:
            raise InvalidContractError("unsupported message version")
        return value

    @classmethod
    def from_json(cls, raw: bytes) -> ContractEnvelope:
        try:
            return cls.model_validate_json(raw)
        except Exception as exc:
            raise InvalidContractError("invalid contract envelope") from exc

    def typed_payload(self) -> StrictPayload:
        model = PAYLOAD_MODELS.get(self.message_type)
        if model is None:
            raise InvalidContractError(f"unsupported message type: {self.message_type}")
        try:
            return model.model_validate(self.payload)
        except Exception as exc:
            raise InvalidContractError("invalid typed contract payload") from exc
