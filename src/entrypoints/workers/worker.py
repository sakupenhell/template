from dishka.integrations.taskiq import setup_dishka

from src.bootstrap.di.container import create_container
from src.entrypoints.workers.tasks.example import ping_redis  # noqa: F401
from src.infrastructure.adapters.taskiq.broker import broker

setup_dishka(container=create_container(), broker=broker)
