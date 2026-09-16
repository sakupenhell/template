from dataclasses import dataclass
from uuid import UUID

from src.application.interfaces.storages.item import IItemStorage
from src.application.interfaces.uow import AbstractUOW
from src.application.use_case import IQuery
from src.domain.entities.item import Item
from src.domain.exceptions import EntityNotFoundException


@dataclass(frozen=True, slots=True, kw_only=True)
class GetItemByIdQuery(IQuery[UUID, Item]):
    uow: AbstractUOW
    item_storage: IItemStorage

    async def execute(self, *, input_dto: UUID) -> Item:
        async with self.uow:
            item = await self.item_storage.fetch_by_id(input_id=input_dto)
        if item is None:
            raise EntityNotFoundException("Item", input_dto)
        return item
