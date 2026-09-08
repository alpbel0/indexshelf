from __future__ import annotations

from collections.abc import Awaitable, Callable

import aio_pika

from indexshelf_data.contracts import ContractEnvelope, InvalidContractError

Handler = Callable[[ContractEnvelope], Awaitable[None]]


async def consume_message(
    message: aio_pika.abc.AbstractIncomingMessage,
    handler: Handler,
    dlq: aio_pika.abc.AbstractExchange | None = None,
    *,
    is_duplicate: Callable[[ContractEnvelope], Awaitable[bool]] | None = None,
    max_attempts: int = 3,
) -> None:
    try:
        envelope = ContractEnvelope.from_json(message.body)
    except InvalidContractError:
        await message.reject(requeue=False)
        return
    if is_duplicate is not None and await is_duplicate(envelope):
        await message.ack()
        return
    try:
        await handler(envelope)
    except Exception:
        headers = message.headers or {}
        raw_retries = headers.get("x-retry-count", 0)
        retries = int(raw_retries) if isinstance(raw_retries, (int, str)) else 0
        raw_delivery_count = headers.get("x-delivery-count")
        broker_retries = (
            int(raw_delivery_count) if isinstance(raw_delivery_count, (int, str)) else 0
        )
        classic_redelivery = message.redelivered and raw_delivery_count is None
        retry_exhausted = (
            retries >= max_attempts - 1
            or broker_retries >= max_attempts - 1
            or classic_redelivery
        )
        if retry_exhausted:
            await message.reject(requeue=False)
        else:
            await message.nack(requeue=True)
        return
    await message.ack()
