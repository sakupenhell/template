from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

from src.config import settings

broker: RedisStreamBroker = RedisStreamBroker(
    url=settings.taskiq.broker_url
).with_result_backend(
    RedisAsyncResultBackend(redis_url=settings.taskiq.result_backend_url)
)
