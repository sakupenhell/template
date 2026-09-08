from typing import ClassVar

from pydantic import BaseModel
from pydantic.fields import Field
from pydantic_settings.main import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    title: str = "API"
    version: str = "0.1.0"
    description: str = ""


class DatabaseSettings(BaseModel):
    name: str = "postgres"
    user: str = "postgres"
    password: str = "postgres"
    host: str = "postgres"
    port: int = 5432

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisSettings(BaseModel):
    host: str = "redis"
    port: int = 6379

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}"


class TaskiqSettings(BaseModel):
    host: str = "redis"
    port: int = 6379
    broker_db: int = 0
    result_backend_db: int = 1

    @property
    def broker_url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.broker_db}"

    @property
    def result_backend_url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.result_backend_db}"


class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
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
