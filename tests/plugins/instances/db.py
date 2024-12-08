from collections.abc import AsyncIterator
from os import environ
from types import SimpleNamespace

import pytest
from alembic.config import Config as AlembicConfig
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from rental_bot.adapters.database.config import DatabaseConfig
from rental_bot.adapters.database.tables import BaseTable
from rental_bot.adapters.database.utils import (
    create_engine,
    create_sessionmaker,
    make_alembic_config,
)
from tests.utils import run_async_migrations, truncate_tables


@pytest.fixture
def db_config() -> DatabaseConfig:
    return DatabaseConfig(
        dsn=environ.get(
            "APP_DATABASE_DSN",
            "postgresql+asyncpg://rental_bot:rental_bot@127.0.0.1:5432/rental_bot",
        ),
    )


@pytest.fixture
def alembic_config(db_config: DatabaseConfig) -> AlembicConfig:
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options, pg_url=db_config.dsn)


@pytest.fixture
async def engine(
    alembic_config: AlembicConfig,
    db_config: DatabaseConfig,
) -> AsyncIterator[AsyncEngine]:
    await run_async_migrations(alembic_config, BaseTable.metadata, "head")
    async with create_engine(
        dsn=db_config.dsn, debug=True, pool_size=10, pool_timeout=10, max_overflow=10
    ) as engine:
        await truncate_tables(engine)

        yield engine


@pytest.fixture
def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return create_sessionmaker(engine=engine)


@pytest.fixture
async def session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session
        await session.rollback()
