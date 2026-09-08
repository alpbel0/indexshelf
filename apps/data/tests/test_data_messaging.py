import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from indexshelf_data.adapters.inbound.rabbitmq.consumer import consume_message
from indexshelf_data.contracts import ContractEnvelope, InvalidContractError
from indexshelf_data.contracts.contract_envelope import Subject


def _payload(kind: str = "command") -> bytes:
    return ContractEnvelope(
        message_id=uuid4(), message_kind=kind, message_type="job.cancel", message_version=1,
        occurred_at=datetime.now(UTC), correlation_id=uuid4(), producer="backend",
        subject=Subject(kind="job", id=uuid4()), payload={"job_id": uuid4(), "reason": "policy"},
    ).model_dump_json().encode()


def test_contract_rejects_unsupported_version() -> None:
    invalid = _payload().replace(b'"message_version":1', b'"message_version":2')
    with pytest.raises(InvalidContractError):
        ContractEnvelope.from_json(invalid)


def test_contract_deserializes_known_payload_to_typed_model() -> None:
    envelope = ContractEnvelope.from_json(_payload())
    payload = envelope.typed_payload()
    assert payload.__class__.__name__ == "CancelJobPayload"


def test_consumer_ack_follows_successful_handler() -> None:
    async def run() -> None:
        message = AsyncMock(body=_payload())
        handler = AsyncMock()
        dlq = AsyncMock()
        await consume_message(message, handler, dlq)
        handler.assert_awaited_once()
        message.ack.assert_awaited_once()
        message.reject.assert_not_awaited()

    asyncio.run(run())


def test_consumer_rejects_classic_redelivery_after_handler_failure() -> None:
    async def run() -> None:
        message = AsyncMock(body=_payload(), redelivered=True, headers={})
        handler = AsyncMock(side_effect=RuntimeError("permanent"))
        await consume_message(message, handler, max_attempts=3)
        message.reject.assert_awaited_once_with(requeue=False)
        message.nack.assert_not_awaited()

    asyncio.run(run())
