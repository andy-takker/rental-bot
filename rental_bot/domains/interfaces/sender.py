from abc import abstractmethod
from typing import Protocol

from rental_bot.domains.entities.bpru import Advert


class IAdvertSender(Protocol):
    @abstractmethod
    async def send_advert(self, advert: Advert) -> None:
        raise NotImplementedError
