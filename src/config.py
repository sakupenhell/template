from pydantic import BaseModel
from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.infrastructure.adapters.redis.config import RedisSettings
from src.infrastructure.adapters.taskiq.config import TaskiqSettings
from src.infrastructure.database.config import DatabaseSettings


class AppSettings(BaseModel):
    title: str = "API"
    version: str = "0.1.0"
    description: str = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )
    app: AppSettings = Field(default_factory=AppSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    taskiq: TaskiqSettings = Field(default_factory=TaskiqSettings)


settings: Settings = Settings()
