from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import cast

import aio_pika


@dataclass(frozen=True, slots=True)
class RabbitMqSettings:
    url: str
    exchange: str = "indexshelf.data.events"
    retry_attempts: int = 3

    def validate(self) -> None:
        if not self.url.startswith(("amqp://", "amqps://")):
            raise ValueError("RabbitMQ URL must use amqp or amqps")
        if not self.exchange or self.retry_attempts < 1:
            raise ValueError("RabbitMQ exchange and retry_attempts are required")


class RabbitMqEventPublisher:
    def __init__(self, settings: RabbitMqSettings) -> None:
        settings.validate()
        self._settings = settings
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractRobustChannel | None = None

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self._settings.url, timeout=10)
        self._channel = cast(aio_pika.abc.AbstractRobustChannel, await self._connection.channel(publisher_confirms=True))
        await self._channel.set_qos(prefetch_count=32)

    async def publish(self, body: bytes, *, routing_key: str, message_id: str) -> None:
        if self._channel is None:
            raise RuntimeError("RabbitMQ publisher is not connected")
        exchange = await self._channel.get_exchange(self._settings.exchange, ensure=False)
        message = aio_pika.Message(
            body=body, message_id=message_id, delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        for attempt in range(self._settings.retry_attempts):
            try:
                await exchange.publish(message, routing_key=routing_key, mandatory=True)
                return
            except (TimeoutError, aio_pika.exceptions.AMQPError):
                if attempt + 1 == self._settings.retry_attempts:
                    raise
                await asyncio.sleep(2**attempt)

    async def close(self) -> None:
        if self._connection is not None:
            await self._connection.close()
