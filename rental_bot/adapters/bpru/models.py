from collections.abc import Sequence
from uuid import UUID

from pydantic import BaseModel


class AdvertSchema(BaseModel):
    id: UUID
    title: str
    metro: str
    apartmentHref: str
    price: str
    images: Sequence[str]


class AdvertPageSchema(BaseModel):
    adverts: Sequence[AdvertSchema]
