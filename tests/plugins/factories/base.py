from datetime import UTC, datetime

from polyfactory import Use
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory


class BaseFactory(SQLAlchemyFactory):
    __is_base_factory__ = True

    created_at = Use(lambda: datetime.now(UTC))
    updated_at = Use(lambda: datetime.now(UTC))
    deleted_at = None
