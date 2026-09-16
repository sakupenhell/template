from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from src.infrastructure.adapters.redis.config import RedisSettings


class RedisProvider(Provider):
    def __init__(self, settings: RedisSettings) -> None:
        super().__init__()
        self._settings: RedisSettings = settings

    @provide(scope=Scope.APP)
    async def client(self) -> AsyncIterator[Redis]:
        redis_client: Redis = Redis.from_url(
            self._settings.url,
            encoding="utf-8",
            decode_responses=False,
            max_connections=self._settings.max_connections,
        )
        yield redis_client
        await redis_client.aclose()
