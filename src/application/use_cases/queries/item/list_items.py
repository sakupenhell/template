from dataclasses import dataclass

from src.application.dto.pagination import (
    PaginatedOutputDTO,
    PaginationInputDTO,
    get_limit_offset,
    get_total_pages,
)
from src.application.interfaces.storages.item import IItemStorage
from src.application.interfaces.uow import AbstractUOW
from src.application.use_case import IQuery
from src.domain.entities.item import Item


@dataclass(frozen=True, slots=True, kw_only=True)
class ListItemsQuery(IQuery[PaginationInputDTO, PaginatedOutputDTO[Item]]):
    uow: AbstractUOW
    item_storage: IItemStorage

    async def execute(self, *, input_dto: PaginationInputDTO) -> PaginatedOutputDTO[Item]:
        limit, offset = get_limit_offset(page=input_dto.page, page_size=input_dto.page_size)
        async with self.uow:
            items = await self.item_storage.fetch_list(limit=limit, offset=offset)
            total = await self.item_storage.count()
        return PaginatedOutputDTO(
            items=items,
            total=total,
            page=input_dto.page,
            page_size=input_dto.page_size,
            total_pages=get_total_pages(total=total, page_size=input_dto.page_size),
        )
