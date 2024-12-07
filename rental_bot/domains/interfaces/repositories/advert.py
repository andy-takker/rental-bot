from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from rental_bot.domains.entities.bpru import Advert, ParsedAdvert


class IAdvertRepository(Protocol):
    @abstractmethod
    async def find_new(self, external_ids: Sequence[str], source: str) -> Sequence[str]:
        raise NotImplementedError

    @abstractmethod
    async def save_many(self, adverts: Sequence[ParsedAdvert]) -> Sequence[Advert]:
        raise NotImplementedError
