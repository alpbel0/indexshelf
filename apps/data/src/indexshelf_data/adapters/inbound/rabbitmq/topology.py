from __future__ import annotations

import aio_pika


async def declare_data_topology(
    channel: aio_pika.abc.AbstractChannel,
) -> aio_pika.abc.AbstractQueue:
    return await channel.get_queue("indexshelf.backend.commands", ensure=True)
