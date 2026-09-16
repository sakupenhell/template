from pydantic import BaseModel


class RedisSettings(BaseModel):
    host: str = "redis"
    port: int = 6379
    max_connections: int = 20

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}"
