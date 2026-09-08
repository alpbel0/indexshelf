import asyncio
import json
import logging

from indexshelf_data.adapters.outbound.messaging.event_outbox import mark_published
from indexshelf_data.adapters.outbound.messaging.rabbitmq_event_publisher import (
    RabbitMqEventPublisher,
    RabbitMqSettings,
)
from indexshelf_data.adapters.outbound.persistence.database import create_session_factory
from indexshelf_data.adapters.outbound.persistence.repositories import EventOutboxRepository
from indexshelf_data.bootstrap.logging import configure_logging
from indexshelf_data.bootstrap.settings import DataSettings

logger = logging.getLogger(__name__)


async def run() -> None:
    settings = DataSettings()
    configure_logging(settings.log_level)
    publisher = RabbitMqEventPublisher(RabbitMqSettings(settings.rabbitmq_url))
    await publisher.connect()
    sessions = create_session_factory(settings.database_url)
    try:
        while True:
            async with sessions() as session:
                async with session.begin():
                    for record in await EventOutboxRepository(session).pending():
                        body = json.dumps(record.payload, separators=(",", ":")).encode("utf-8")
                        await publisher.publish(
                            body,
                            routing_key=record.event_type,
                            message_id=str(record.event_id),
                        )
                        await mark_published(session, record.event_id)
            await asyncio.sleep(1)
    finally:
        await publisher.close()


if __name__ == "__main__":
    asyncio.run(run())
