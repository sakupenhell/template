from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    name: str = "postgres"
    user: str = "postgres"
    password: str = "postgres"
    host: str = "postgres"
    port: int = 5432
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    echo: bool = False

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
