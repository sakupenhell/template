from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider
from dishka.integrations.taskiq import TaskiqProvider

from src.bootstrap.di.application import ApplicationProvider
from src.bootstrap.di.database import DatabaseProvider
from src.bootstrap.di.redis import RedisProvider
from src.bootstrap.di.taskiq import TaskiqProvider as BrokerProvider
from src.config import settings


def create_container() -> AsyncContainer:
    return make_async_container(
        FastapiProvider(),
        DatabaseProvider(settings.db),
        RedisProvider(settings.redis),
        BrokerProvider(settings.taskiq),
        ApplicationProvider(),
        TaskiqProvider(),
    )
