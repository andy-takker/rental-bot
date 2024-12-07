from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from textwrap import dedent
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class Advert:
    id: UUID
    title: str
    url: str
    source: str
    external_id: str
    price: int
    properties: Mapping[str, Any]

    def to_message(self) -> str:
        return dedent(
            f"Найдена новая квартира:\n"
            f"{self.title}\n"
            f"{self.price} р.\n"
            f"{self.metro}\n"
            f"{self.url}"
        )

    @property
    def metro(self) -> str:
        return self.properties.get("metro", "")

    @property
    def images(self) -> Sequence[str]:
        return self.properties.get("images", [])


@dataclass(frozen=True, slots=True, kw_only=True)
class ParsedAdvert:
    title: str
    url: str
    source: str
    external_id: str
    price: int
    properties: Mapping[str, Any]
