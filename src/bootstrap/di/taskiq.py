from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from taskiq import AsyncBroker

from src.infrastructure.adapters.taskiq.broker import broker
from src.infrastructure.adapters.taskiq.config import TaskiqSettings


class TaskiqProvider(Provider):
    def __init__(self, settings: TaskiqSettings) -> None:
        super().__init__()
        self._settings: TaskiqSettings = settings

    @provide(scope=Scope.APP)
    async def broker(self) -> AsyncIterator[AsyncBroker]:
        await broker.startup()
        try:
            yield broker
        finally:
            await broker.shutdown()
