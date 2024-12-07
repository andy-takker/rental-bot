import logging
from asyncio import sleep

from dishka import AsyncContainer

from rental_bot.domains.use_cases.parse_adverts import ParseAdvertsUseCase

log = logging.getLogger(__name__)


async def start_monitoring(container: AsyncContainer, sleep_time: int) -> None:
    log.info("Start monitoring BPRU")
    while True:
        async with container() as cont:
            parse_adverts = await cont.get(ParseAdvertsUseCase)
            await parse_adverts.execute()
        await sleep(sleep_time)
