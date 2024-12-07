from collections.abc import AsyncIterator

from dishka import AnyOf, BaseScope, Provider, Scope, provide
from dishka.entities.component import Component
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from rental_bot.adapters.database.config import DatabaseConfig
from rental_bot.adapters.database.repositories.advert import AdvertRepository
from rental_bot.adapters.database.uow import SqlalchemyUow
from rental_bot.adapters.database.utils import create_engine, create_sessionmaker
from rental_bot.domains.interfaces.repositories.advert import IAdvertRepository
from rental_bot.domains.uow import AbstractUow


class DatabaseProvider(Provider):
    __config: DatabaseConfig
    __debug: bool

    def __init__(
        self,
        config: DatabaseConfig,
        debug: bool,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ) -> None:
        self.__config = config
        self.__debug = debug
        super().__init__(scope=scope, component=component)

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        async with create_engine(
            dsn=self.__config.dsn,
            pool_size=self.__config.pool_size,
            pool_timeout=self.__config.pool_timeout,
            max_overflow=self.__config.max_overflow,
            debug=self.__debug,
        ) as engine:
            yield engine

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_sessionmaker(engine=engine)

    @provide(scope=Scope.REQUEST)
    def uow(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AnyOf[AbstractUow, SqlalchemyUow]:
        return SqlalchemyUow(session=session_factory())

    @provide(scope=Scope.REQUEST)
    def advert_repository(
        self, uow: SqlalchemyUow
    ) -> AnyOf[IAdvertRepository, AdvertRepository]:
        return AdvertRepository(session=uow.session)
