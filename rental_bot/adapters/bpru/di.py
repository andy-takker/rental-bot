from collections.abc import AsyncIterator

import aiohttp
from dishka import AnyOf, Provider, Scope, provide

from rental_bot.adapters.bpru.client import BpruClient
from rental_bot.domains.interfaces.client import IAdvertClient


class BpruProvider(Provider):
    @provide(scope=Scope.APP)
    async def bpru_client(self) -> AsyncIterator[AnyOf[IAdvertClient, BpruClient]]:
        async with aiohttp.ClientSession() as session:
            yield BpruClient(
                session=session,
                url="https://bpru.ru",
                client_name="bpru",
            )
