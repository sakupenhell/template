from dataclasses import dataclass

from src.application.dto.item import CreateItemDTO
from src.application.interfaces.storages.item import IItemStorage
from src.application.interfaces.uow import AbstractUOW
from src.application.use_case import ICommand
from src.domain.entities.item import Item


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateItemCommand(ICommand[CreateItemDTO, Item]):
    uow: AbstractUOW
    item_storage: IItemStorage

    async def execute(self, *, input_dto: CreateItemDTO) -> Item:
        async with self.uow:
            return await self.item_storage.create(input_dto=input_dto)
