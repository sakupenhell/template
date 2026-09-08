from taskiq_redis import RedisStreamBroker

from src.config import settings

broker: RedisStreamBroker = RedisStreamBroker(url=settings.taskiq.broker_url)
