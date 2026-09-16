from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from enum import Enum

from sqlalchemy import Enum as SAEnum
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.infrastructure.database.config import DatabaseSettings


@asynccontextmanager
async def create_engine(config: DatabaseSettings) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        url=config.url,
        echo=config.echo,
        pool_size=config.pool_size,
        max_overflow=config.max_overflow,
        pool_timeout=config.pool_timeout,
        connect_args={
            "statement_cache_size": 0,
        },
    )
    yield engine
    await engine.dispose()


def str_enum_column(enum_cls: type[Enum], *, name: str) -> SAEnum:
    return SAEnum(
        enum_cls,
        name=name,
        native_enum=False,
        create_constraint=True,
        values_callable=lambda enum: [member.value for member in enum],
    )
