import os
import asyncio
from datetime import timedelta

import pytest

from indexshelf_data.adapters.outbound.cache.valkey_cache import ValkeyCache
from indexshelf_data.adapters.outbound.messaging.rabbitmq_event_publisher import (
    RabbitMqEventPublisher,
    RabbitMqSettings,
)
from indexshelf_data.adapters.outbound.storage.s3_temporary_object_storage import (
    ObjectStorageSettings,
    S3TemporaryObjectStorage,
)


def test_live_adapters() -> None:
    if os.getenv("INDEXSHELF_RUN_DATA_ADAPTER_SMOKE") != "1":
        pytest.skip("live local stack smoke is opt-in")
    async def run() -> None:
        publisher = RabbitMqEventPublisher(RabbitMqSettings(os.environ["INDEXSHELF_RABBIT_URL"]))
        await publisher.connect()
        await publisher.publish(b"smoke", routing_key="data.events", message_id="smoke-1")
        await publisher.close()
        storage = S3TemporaryObjectStorage(ObjectStorageSettings(os.environ["INDEXSHELF_MINIO_ENDPOINT"], "indexshelf_minio_root", "indexshelf_minio_root_dummy_password", "indexshelf-temporary"))
        await storage.put("smoke/1.txt", b"smoke", "text/plain")
        assert "X-Amz" in await storage.presigned_get("smoke/1.txt")
        from redis.asyncio import Redis
        cache = ValkeyCache(Redis.from_url(os.environ["INDEXSHELF_VALKEY_URL"]))
        await cache.set("smoke", b"ok", timedelta(seconds=30))
        assert await cache.get("smoke") == b"ok"
        await cache._client.aclose()
    asyncio.run(run())
