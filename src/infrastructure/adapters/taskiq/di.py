from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from taskiq import AsyncBroker

from src.infrastructure.adapters.taskiq.broker import broker


class TaskiqProvider(Provider):
    @provide(scope=Scope.APP)
    async def broker(self) -> AsyncIterator[AsyncBroker]:
        await broker.startup()
        try:
            yield broker
        finally:
            await broker.shutdown()
