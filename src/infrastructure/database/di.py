from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from src.config import DatabaseSettings


class DatabaseProvider(Provider):
    def __init__(self, config: DatabaseSettings) -> None:
        super().__init__()
        self._config: DatabaseSettings = config

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        engine: AsyncEngine = create_async_engine(
            url=self._config.url,
            echo=False,
            pool_size=20,
            max_overflow=40,
            pool_timeout=30,
            pool_recycle=1800,
            connect_args={
                "prepared_statement_cache_size": 100,
            },
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.REQUEST)
    async def connection(self, engine: AsyncEngine) -> AsyncIterator[AsyncConnection]:
        async with engine.begin() as connection:
            yield connection
