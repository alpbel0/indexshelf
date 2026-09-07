import asyncio
import logging

from indexshelf_data.bootstrap.logging import configure_logging
from indexshelf_data.bootstrap.settings import DataSettings

logger = logging.getLogger(__name__)


async def run() -> None:
    settings = DataSettings()
    configure_logging(settings.log_level)
    logger.warning("Data outbox relay bootstrap is running; no relay pipeline is configured yet.")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(run())
