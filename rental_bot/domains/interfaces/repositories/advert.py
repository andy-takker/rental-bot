from abc import abstractmethod
from collections.abc import Iterable, Sequence, Set
from typing import Protocol

from rental_bot.domains.entities.bpru import Advert, ParsedAdvert


class IAdvertRepository(Protocol):
    @abstractmethod
    async def find_new(self, external_ids: Iterable[str], source: str) -> Set[str]:
        raise NotImplementedError

    @abstractmethod
    async def save_many(self, adverts: Sequence[ParsedAdvert]) -> Sequence[Advert]:
        raise NotImplementedError
