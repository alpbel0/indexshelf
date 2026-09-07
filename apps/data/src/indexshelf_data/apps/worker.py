import asyncio
import logging

from indexshelf_data.apps.worker_profile import profile_from_environment
from indexshelf_data.bootstrap.logging import configure_logging
from indexshelf_data.bootstrap.settings import DataSettings

logger = logging.getLogger(__name__)


async def run() -> None:
    settings = DataSettings()
    configure_logging(settings.log_level)
    profile = profile_from_environment()
    logger.warning(
        "Data worker profile '%s' is running; no processing pipeline is configured yet.",
        profile.name,
    )
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(run())
