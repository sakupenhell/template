from pydantic import BaseModel


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
