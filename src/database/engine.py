from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.config import settings

engine: AsyncEngine = create_async_engine(
    url=settings.db.url,
    echo=False,
    pool_size=20,
    max_overflow=40,
    pool_timeout=30,
    pool_recycle=1800,
    connect_args={
        "prepared_statement_cache_size": 100,
    },
)
