from collections.abc import Iterable, Sequence, Set

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from rental_bot.adapters.database.tables import AdvertTable
from rental_bot.domains.entities.bpru import Advert, ParsedAdvert
from rental_bot.domains.interfaces.repositories.advert import IAdvertRepository


class AdvertRepository(IAdvertRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def find_new(self, external_ids: Iterable[str], source: str) -> Set[str]:
        stmt = (
            select(AdvertTable.external_id)
            .where(AdvertTable.source == source)
            .where(AdvertTable.external_id.in_(external_ids))
        )
        saved_ids = await self.__session.scalars(stmt)
        return set(external_ids) - set(saved_ids)

    async def save_many(self, adverts: Sequence[ParsedAdvert]) -> Sequence[Advert]:
        if not adverts:
            return []
        stmt = (
            insert(AdvertTable)
            .values(
                [
                    {
                        "title": advert.title,
                        "url": advert.url,
                        "price": advert.price,
                        "source": advert.source,
                        "external_id": advert.external_id,
                        "properties": advert.properties,
                    }
                    for advert in adverts
                ]
            )
            .returning(AdvertTable)
        )

        result = await self.__session.scalars(stmt)
        return [
            Advert(
                id=row.id,
                title=row.title,
                url=row.url,
                price=row.price,
                source=row.source,
                external_id=row.external_id,
                properties=row.properties,
            )
            for row in result
        ]
