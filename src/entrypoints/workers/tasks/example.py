import logging

from dishka import FromDishka
from dishka.integrations.taskiq import inject
from redis.asyncio import Redis

from src.infrastructure.adapters.taskiq.broker import broker

log = logging.getLogger(__name__)


@broker.task
@inject
async def ping_redis(redis: FromDishka[Redis]) -> None:
    await redis.incr("taskiq:ping:count")
    log.info("ping_redis task executed")
