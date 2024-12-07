from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from rental_bot.domains.entities.bpru import ParsedAdvert


class IAdvertClient(Protocol):
    @abstractmethod
    async def fetch_adverts(self) -> Sequence[ParsedAdvert]:
        raise NotImplementedError
