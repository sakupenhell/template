from uuid import UUID

from sqlalchemy import func, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection

from src.application.dto.item import CreateItemDTO, UpdateItemDTO
from src.application.interfaces.storages.item import IItemStorage
from src.domain.entities.item import Item
from src.domain.exceptions import EntityAlreadyExistsException, EntityNotFoundException
from src.infrastructure.database.converters.item import convert_row_to_item
from src.infrastructure.database.tables.item import items_table

_UNIQUE_TITLE_CONSTRAINT = "uq__items__title"


class ItemStorage(IItemStorage):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def fetch_by_id(self, *, input_id: UUID) -> Item | None:
        stmt = select(items_table).where(items_table.c.id == input_id)
        result = await self._connection.execute(stmt)
        row = result.one_or_none()
        return convert_row_to_item(row) if row is not None else None

    async def fetch_list(self, *, limit: int, offset: int) -> list[Item]:
        stmt = (
            select(items_table)
            .order_by(items_table.c.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        rows = (await self._connection.execute(stmt)).all()
        return [convert_row_to_item(row) for row in rows]

    async def count(self) -> int:
        stmt = select(func.count()).select_from(items_table)
        return (await self._connection.execute(stmt)).scalar_one()

    async def create(self, *, input_dto: CreateItemDTO) -> Item:
        stmt = (
            insert(items_table)
            .values(title=input_dto.title, description=input_dto.description)
            .returning(items_table)
        )
        try:
            result = await self._connection.execute(stmt)
        except IntegrityError as exc:
            if _UNIQUE_TITLE_CONSTRAINT in str(exc.orig):
                raise EntityAlreadyExistsException("Item", input_dto.title) from exc
            raise
        return convert_row_to_item(result.one())

    async def update_by_id(self, *, input_id: UUID, input_dto: UpdateItemDTO) -> Item:
        values = {
            key: value
            for key, value in (
                ("title", input_dto.title),
                ("description", input_dto.description),
            )
            if value is not None
        }
        if not values:
            existing = await self.fetch_by_id(input_id=input_id)
            if existing is None:
                raise EntityNotFoundException("Item", input_id)
            return existing
        stmt = (
            update(items_table)
            .where(items_table.c.id == input_id)
            .values(**values)
            .returning(items_table)
        )
        try:
            result = await self._connection.execute(stmt)
        except IntegrityError as exc:
            if _UNIQUE_TITLE_CONSTRAINT in str(exc.orig):
                raise EntityAlreadyExistsException("Item", input_dto.title) from exc
            raise
        row = result.one_or_none()
        if row is None:
            raise EntityNotFoundException("Item", input_id)
        return convert_row_to_item(row)

    async def delete_by_id(self, *, input_id: UUID) -> None:
        stmt = (
            items_table.delete()
            .where(items_table.c.id == input_id)
            .returning(items_table.c.id)
        )
        result = await self._connection.execute(stmt)
        try:
            result.one()
        except NoResultFound as exc:
            raise EntityNotFoundException("Item", input_id) from exc
