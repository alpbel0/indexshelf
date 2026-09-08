import asyncio
import os
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import aio_pika
import pytest

from indexshelf_data.adapters.inbound.rabbitmq.consumer import consume_message
from indexshelf_data.adapters.outbound.cache.valkey_cache import ValkeyCache
from indexshelf_data.adapters.outbound.messaging.rabbitmq_event_publisher import (
    RabbitMqEventPublisher,
    RabbitMqSettings,
)
from indexshelf_data.adapters.outbound.storage.s3_temporary_object_storage import (
    ObjectStorageSettings,
    S3TemporaryObjectStorage,
)
from indexshelf_data.contracts import ContractEnvelope
from indexshelf_data.contracts.contract_envelope import Subject


def test_live_adapters() -> None:
    if os.getenv("INDEXSHELF_RUN_DATA_ADAPTER_SMOKE") != "1":
        pytest.skip("live local stack smoke is opt-in")
    async def run() -> None:
        publisher = RabbitMqEventPublisher(RabbitMqSettings(os.environ["INDEXSHELF_RABBIT_URL"]))
        await publisher.connect()
        await publisher.publish(b"smoke", routing_key="data.events", message_id="smoke-1")
        await publisher.close()
        storage = S3TemporaryObjectStorage(
            ObjectStorageSettings(
                os.environ["INDEXSHELF_MINIO_ENDPOINT"],
                "indexshelf_minio_root",
                "indexshelf_minio_root_dummy_password",
                "indexshelf-temporary",
            )
        )
        await storage.put("smoke/1.txt", b"smoke", "text/plain")
        assert "X-Amz" in await storage.presigned_get("smoke/1.txt")
        from redis.asyncio import Redis
        cache = ValkeyCache(Redis.from_url(os.environ["INDEXSHELF_VALKEY_URL"]))
        await cache.set("smoke", b"ok", timedelta(seconds=30))
        assert await cache.get("smoke") == b"ok"
        await cache._client.aclose()
    asyncio.run(run())


def test_live_rabbitmq_redelivery_and_duplicate_suppression() -> None:
    if os.getenv("INDEXSHELF_RUN_RABBIT_INTEGRATION") != "1":
        pytest.skip("live RabbitMQ integration is opt-in")

    async def run() -> None:
        body = ContractEnvelope(
            message_id=uuid4(),
            message_kind="command",
            message_type="job.cancel",
            message_version=1,
            occurred_at=datetime.now(UTC),
            correlation_id=uuid4(),
            producer="backend",
            subject=Subject(kind="job", id=uuid4()),
            payload={"job_id": str(uuid4()), "reason": "policy"},
        ).model_dump_json().encode()
        publisher = await aio_pika.connect_robust(os.environ["INDEXSHELF_RABBIT_BACKEND_URL"])
        publisher_channel = await publisher.channel(publisher_confirms=True)
        exchange = await publisher_channel.get_exchange("indexshelf.backend.commands", ensure=False)
        consumer = await aio_pika.connect_robust(os.environ["INDEXSHELF_RABBIT_DATA_URL"])
        consumer_channel = await consumer.channel()
        queue = await consumer_channel.get_queue("indexshelf.backend.commands", ensure=False)
        try:
            await exchange.publish(aio_pika.Message(body=body), routing_key="job.cancel")
            first = await _get_matching(queue, body)
            calls = 0

            async def failing_handler(_envelope: ContractEnvelope) -> None:
                nonlocal calls
                calls += 1
                raise RuntimeError("integration retry")

            await consume_message(first, failing_handler, max_attempts=3)
            await consumer.close()
            consumer = await aio_pika.connect_robust(os.environ["INDEXSHELF_RABBIT_DATA_URL"])
            consumer_channel = await consumer.channel()
            queue = await consumer_channel.get_queue("indexshelf.backend.commands", ensure=False)
            second = await _get_matching(queue, body)
            await consume_message(second, failing_handler, max_attempts=3)
            assert calls == 2

            await exchange.publish(aio_pika.Message(body=body), routing_key="job.cancel")
            duplicate = await _get_matching(queue, body)
            seen = {ContractEnvelope.from_json(body).message_id}
            await consume_message(
                duplicate,
                failing_handler,
                is_duplicate=lambda envelope: _duplicate(seen, envelope),
            )
            assert calls == 2
        finally:
            await consumer.close()
            await publisher.close()

    asyncio.run(run())


async def _duplicate(seen: set[UUID], envelope: ContractEnvelope) -> bool:
    return envelope.message_id in seen


async def _get_matching(
    queue: aio_pika.abc.AbstractQueue,
    body: bytes,
) -> aio_pika.abc.AbstractIncomingMessage:
    while True:
        message = await queue.get(timeout=5)
        if message.body == body:
            return message
        await message.ack()
