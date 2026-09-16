from dishka import AsyncContainer, make_async_container

from src.config import settings
from src.infrastructure.adapters.redis.di import RedisProvider
from src.infrastructure.adapters.taskiq.di import TaskiqProvider
from src.infrastructure.database.di import DatabaseProvider


def create_container() -> AsyncContainer:
    return make_async_container(
        DatabaseProvider(settings.db),
        RedisProvider(settings.redis),
        TaskiqProvider(),
        skip_validation=True,
    )
