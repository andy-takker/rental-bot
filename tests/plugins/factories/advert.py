from collections.abc import Awaitable, Callable

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from rental_bot.adapters.database.tables import AdvertTable
from tests.plugins.factories.base import BaseFactory


@pytest.fixture
def create_advert(session: AsyncSession) -> Callable[..., Awaitable[AdvertTable]]:
    class AdvertTableFactory(BaseFactory):
        __model__ = AdvertTable
        __async_session__ = session

    return AdvertTableFactory.create_async
