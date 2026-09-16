from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from src.application.dto.item import CreateItemDTO, UpdateItemDTO
from src.application.dto.pagination import (
    DEFAULT_PAGE_SIZE,
    MIN_PAGE,
    PaginationInputDTO,
)
from src.application.use_cases.commands.item.create import CreateItemCommand
from src.application.use_cases.commands.item.delete import DeleteItemCommand
from src.application.use_cases.commands.item.update import UpdateItemCommand
from src.application.use_cases.queries.item.get_by_id import GetItemByIdQuery
from src.application.use_cases.queries.item.list_items import ListItemsQuery
from src.entrypoints.http.api.v1.schemas.item import (
    CreateItemRequestSchema,
    ItemResponseSchema,
    PaginatedItemsResponseSchema,
    UpdateItemRequestSchema,
)

item_router = APIRouter(prefix="/items", tags=["items"], route_class=DishkaRoute)


@item_router.post("", status_code=status.HTTP_201_CREATED)
async def create_item(
    body: CreateItemRequestSchema,
    command: FromDishka[CreateItemCommand],
) -> ItemResponseSchema:
    item = await command.execute(
        input_dto=CreateItemDTO(title=body.title, description=body.description)
    )
    return ItemResponseSchema.from_entity(item)


@item_router.get("")
async def list_items(
    query: FromDishka[ListItemsQuery],
    page: int = MIN_PAGE,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> PaginatedItemsResponseSchema:
    result = await query.execute(
        input_dto=PaginationInputDTO(page=page, page_size=page_size)
    )
    return PaginatedItemsResponseSchema(
        items=[ItemResponseSchema.from_entity(item) for item in result.items],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
        total_pages=result.total_pages,
    )


@item_router.get("/{item_id}")
async def get_item(
    item_id: UUID, query: FromDishka[GetItemByIdQuery]
) -> ItemResponseSchema:
    item = await query.execute(input_dto=item_id)
    return ItemResponseSchema.from_entity(item)


@item_router.patch("/{item_id}")
async def update_item(
    item_id: UUID,
    body: UpdateItemRequestSchema,
    command: FromDishka[UpdateItemCommand],
) -> ItemResponseSchema:
    item = await command.execute(
        input_dto=UpdateItemDTO(
            item_id=item_id, title=body.title, description=body.description
        )
    )
    return ItemResponseSchema.from_entity(item)


@item_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: UUID, command: FromDishka[DeleteItemCommand]) -> None:
    await command.execute(input_dto=item_id)
