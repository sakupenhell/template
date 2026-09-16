from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from src.application.interfaces.uow import AbstractUOW
from src.infrastructure.database.config import DatabaseSettings
from src.infrastructure.database.uow import SQLAlchemyUOW
from src.infrastructure.database.utils import create_engine


class DatabaseProvider(Provider):
    def __init__(self, config: DatabaseSettings) -> None:
        super().__init__()
        self._config = config

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        async with create_engine(self._config) as engine:
            yield engine

    @provide(scope=Scope.REQUEST)
    async def connection(self, engine: AsyncEngine) -> AsyncIterator[AsyncConnection]:
        async with engine.connect() as connection:
            yield connection

    @provide(scope=Scope.REQUEST)
    def uow(self, connection: AsyncConnection) -> AbstractUOW:
        return SQLAlchemyUOW(connection)
