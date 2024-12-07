import json
import logging
from collections.abc import Sequence
from http import HTTPStatus
from types import MappingProxyType
from typing import Any

from asyncly import BaseHttpClient, ResponseHandlersType
from asyncly.client.handlers.pydantic import parse_model

from rental_bot.adapters.bpru.models import AdvertPageSchema, AdvertSchema
from rental_bot.domains.entities.bpru import ParsedAdvert
from rental_bot.domains.interfaces.client import IAdvertClient

log = logging.getLogger(__name__)


class BpruClient(IAdvertClient, BaseHttpClient):
    FETCH_ADVERT_PAGE_HANDLERS: ResponseHandlersType = MappingProxyType(
        {
            HTTPStatus.OK: parse_model(AdvertPageSchema),
        }
    )

    async def fetch_adverts(self) -> Sequence[ParsedAdvert]:
        filters = {
            "minPrice": 3000,
            "maxPrice": 100_000,
            "minArea": 35,
            "maxArea": None,
            "minKitchenArea": None,
            "maxKitchenArea": None,
            "minFloor": None,
            "maxFloor": None,
            "buildingMaterials": [],
            "features": [],
            "regions": [],
            "cities": ["54316e13-f046-4447-b633-22be1d77467f"],
            "metro": [
                "b92d86bf-0438-49f8-bfad-f8060d628063",
                "f2b06212-75b4-40cc-94e2-e2121b6e091d",
                "f0329a41-7536-47e5-b0ef-31d5683a3659",
                "93f41f2c-13c2-4164-8732-eb9deba0ec8a",
                "bc66e74a-2230-46e2-bfb1-76ffbaff111e",
                "4a669305-29b3-4520-902b-946174313adf",
            ],
            "roomCounts": ["2", "3"],
            "sortType": "descDate",
            "fullMode": False,
            "notFirstFloor": True,
            "notLastFloor": True,
            "discountOnly": False,
            "photoOnly": True,
            "checkedOnly": True,
            "utilitiesOnly": False,
            "nonDepositOnly": False,
            "dealType": "",
            "realtySubtype": "Flat",
        }
        params = {"filter": json.dumps(filters)}
        page = 0
        adverts: list[AdvertSchema] = []
        while True:
            page += 1
            advert_page = await self.fetch_advert_page(page, params)
            if len(advert_page.adverts) == 0:
                break
            adverts.extend(advert_page.adverts)
        log.info("Got %d adverts", len(adverts))
        return self._convert_adverts_to_entities(adverts)

    async def fetch_advert_page(
        self, page: int, params: dict[str, Any]
    ) -> AdvertPageSchema:
        params["advertPage"] = page
        return await self._make_req(
            method="GET",
            url=self._url / "CatalogRent/GetFlats",
            handlers=self.FETCH_ADVERT_PAGE_HANDLERS,
            params=params,
        )

    def _convert_adverts_to_entities(
        self, adverts: Sequence[AdvertSchema]
    ) -> Sequence[ParsedAdvert]:
        return [
            ParsedAdvert(
                title=advert.title.strip(),
                source="bpru.ru",
                external_id=str(advert.id),
                url=str(self._url) + advert.apartmentHref,
                price=parse_price(advert.price),
                properties={
                    "metro": advert.metro.strip(),
                    "images": [str(self._url) + image for image in advert.images],
                },
            )
            for advert in adverts
        ]


def parse_price(price: str) -> int:
    return int(price.replace(" ", "").replace("\xa0", ""))
