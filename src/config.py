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
    user: str = "posttgres"
    password: str = "postgres"
    host: str = "postgres"
    port: int = 5432

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="_",
    )
    app: AppSettings = Field(default_factory=AppSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)


settings: Settings = Settings()
