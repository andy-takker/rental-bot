from collections.abc import Mapping
from typing import Any

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from rental_bot.adapters.database.base import (
    BaseTable,
    IdentifableMixin,
    TimestampedMixin,
)


class AdvertTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "adverts"

    title: Mapped[str] = mapped_column(String(512), nullable=False)
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    price: Mapped[int] = mapped_column(Integer(), nullable=False)
    source: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    external_id: Mapped[str] = mapped_column(String(63), nullable=False, index=True)
    properties: Mapped[Mapping[str, Any]] = mapped_column(JSONB(), nullable=False)
