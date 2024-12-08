import logging
from dataclasses import dataclass

from rental_bot.application.use_case import IUseCase
from rental_bot.domains.interfaces.client import IAdvertClient
from rental_bot.domains.interfaces.repositories.advert import IAdvertRepository
from rental_bot.domains.interfaces.sender import IAdvertSender
from rental_bot.domains.uow import AbstractUow

log = logging.getLogger(__name__)


@dataclass
class ParseAdvertsUseCase(IUseCase[None, None]):
    uow: AbstractUow
    client: IAdvertClient
    repository: IAdvertRepository
    sender: IAdvertSender

    async def execute(self, *, input_dto: None = None) -> None:
        source = "bpru.ru"
        log.info("Get adverts from BPRU")
        adverts = await self.client.fetch_adverts()
        log.info("Found %d adverts", len(adverts))
        if not adverts:
            log.info("No new adverts")
            return
        async with self.uow:
            new_advert_ids = await self.repository.find_new(
                external_ids={advert.external_id for advert in adverts}, source=source
            )
            log.info("Found %d new adverts", len(new_advert_ids))
            new_adverts = [
                advert for advert in adverts if advert.external_id in new_advert_ids
            ]

            saved_adverts = await self.repository.save_many(new_adverts)
            for advert in saved_adverts:
                await self.sender.send_advert(advert=advert)
            log.info("Done")
