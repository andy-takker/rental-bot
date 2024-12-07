import asyncio

from dishka import make_async_container

from rental_bot.adapters.bpru.di import BpruProvider
from rental_bot.adapters.database.di import DatabaseProvider
from rental_bot.adapters.telegram.di import TelegramProvider
from rental_bot.application.logging import setup_logging
from rental_bot.domains.di import DomainProvider
from rental_bot.presentors.parser.config import ParserConfig
from rental_bot.presentors.parser.manager import ParserManager


async def main() -> None:
    config = ParserConfig()
    setup_logging()
    container = make_async_container(
        BpruProvider(),
        TelegramProvider(config=config.telegram),
        DomainProvider(),
        DatabaseProvider(config=config.database, debug=False),
    )

    manager = ParserManager(container)
    try:
        await manager.start()
    finally:
        manager.stop()
        await container.close()


if __name__ == "__main__":
    asyncio.run(main())
