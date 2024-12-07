from dishka import Provider, Scope, provide

from rental_bot.domains.interfaces.client import IAdvertClient
from rental_bot.domains.interfaces.repositories.advert import IAdvertRepository
from rental_bot.domains.interfaces.sender import IAdvertSender
from rental_bot.domains.uow import AbstractUow
from rental_bot.domains.use_cases.parse_adverts import ParseAdvertsUseCase


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def parse_adverts(
        self,
        client: IAdvertClient,
        repository: IAdvertRepository,
        sender: IAdvertSender,
        uow: AbstractUow,
    ) -> ParseAdvertsUseCase:
        return ParseAdvertsUseCase(
            client=client,
            repository=repository,
            sender=sender,
            uow=uow,
        )
