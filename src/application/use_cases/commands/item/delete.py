from dataclasses import dataclass
from uuid import UUID

from src.application.interfaces.storages.item import IItemStorage
from src.application.interfaces.uow import AbstractUOW
from src.application.use_case import ICommand


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteItemCommand(ICommand[UUID, None]):
    uow: AbstractUOW
    item_storage: IItemStorage

    async def execute(self, *, input_dto: UUID) -> None:
        async with self.uow:
            await self.item_storage.delete_by_id(input_id=input_dto)
