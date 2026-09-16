from datetime import datetime
from uuid import UUID

from src.domain.entities.item import Item
from src.entrypoints.http.schemas import BaseSchema


class CreateItemRequestSchema(BaseSchema):
    title: str
    description: str | None = None


class UpdateItemRequestSchema(BaseSchema):
    title: str | None = None
    description: str | None = None


class ItemResponseSchema(BaseSchema):
    id: UUID
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, item: Item) -> "ItemResponseSchema":
        return cls.model_validate(item)


class PaginatedItemsResponseSchema(BaseSchema):
    items: list[ItemResponseSchema]
    total: int
    page: int
    page_size: int
    total_pages: int
