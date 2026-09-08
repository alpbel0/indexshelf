from __future__ import annotations

from typing import cast

import aio_pika


class RabbitMqConsumerConnection:
    def __init__(self, url: str) -> None:
        if not url.startswith(("amqp://", "amqps://")):
            raise ValueError("RabbitMQ URL must use amqp or amqps")
        self.url = url
        self.connection: aio_pika.abc.AbstractRobustConnection | None = None

    async def connect(self) -> aio_pika.abc.AbstractRobustChannel:
        self.connection = await aio_pika.connect_robust(self.url, timeout=10)
        channel = await self.connection.channel()
        await channel.set_qos(prefetch_count=16)
        return cast(aio_pika.abc.AbstractRobustChannel, channel)

    async def close(self) -> None:
        if self.connection is not None:
            await self.connection.close()
