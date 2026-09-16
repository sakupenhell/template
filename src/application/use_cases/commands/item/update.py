from dataclasses import dataclass

from src.application.dto.item import UpdateItemDTO
from src.application.interfaces.storages.item import IItemStorage
from src.application.interfaces.uow import AbstractUOW
from src.application.use_case import ICommand
from src.domain.entities.item import Item


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateItemCommand(ICommand[UpdateItemDTO, Item]):
    uow: AbstractUOW
    item_storage: IItemStorage

    async def execute(self, *, input_dto: UpdateItemDTO) -> Item:
        async with self.uow:
            return await self.item_storage.update_by_id(
                input_id=input_dto.item_id, input_dto=input_dto
            )
