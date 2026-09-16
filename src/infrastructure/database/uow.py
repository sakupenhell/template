from typing import Any

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncTransaction

from src.application.interfaces.uow import AbstractUOW


class SQLAlchemyUOW(AbstractUOW):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection
        self._transaction: AsyncTransaction | None = None

    async def commit(self) -> None:
        if self._transaction is not None and self._transaction.is_active:
            await self._transaction.commit()
            self._transaction = None
        elif self._connection.in_transaction():
            await self._connection.commit()

    async def rollback(self) -> None:
        if self._transaction is not None and self._transaction.is_active:
            await self._transaction.rollback()
            self._transaction = None
        elif self._connection.in_transaction():
            await self._connection.rollback()

    async def create_transaction(self) -> None:
        if self._transaction is None and not self._connection.in_transaction():
            self._transaction = await self._connection.begin()

    async def close_transaction(self, *exc: Any) -> None:
        if self._transaction is not None and self._transaction.is_active:
            await self._transaction.rollback()
        self._transaction = None
