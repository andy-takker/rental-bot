import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from rental_bot.adapters.database.repositories.advert import AdvertRepository


@pytest.fixture
def advert_repository(session: AsyncSession) -> AdvertRepository:
    return AdvertRepository(session=session)
