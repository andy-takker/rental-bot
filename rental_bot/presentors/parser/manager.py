import asyncio
import logging
from typing import ClassVar

from dishka import AsyncContainer

from rental_bot.presentors.parser import bpru

log = logging.getLogger(__name__)


class ParserManager:
    BPRU_SLEEP_TIME: ClassVar[int] = 60

    def __init__(self, container: AsyncContainer) -> None:
        self.__container = container
        self.__tasks: list[asyncio.Task] = []

    async def start(self) -> None:
        log.info("Start parser manager")
        task = asyncio.create_task(
            bpru.start_monitoring(
                container=self.__container,
                sleep_time=self.BPRU_SLEEP_TIME,
            )
        )

        self.__tasks.append(task)

        while True:
            await asyncio.sleep(1)

    def stop(self) -> None:
        log.info("Stop parser manager")
        for task in self.__tasks:
            task.cancel()
