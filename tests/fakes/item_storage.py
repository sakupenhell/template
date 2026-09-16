from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.application.dto.item import CreateItemDTO, UpdateItemDTO
from src.domain.entities.item import Item
from src.domain.exceptions import EntityAlreadyExistsException, EntityNotFoundException


class FakeItemStorage:
    def __init__(self) -> None:
        self.items: list[Item] = []

    async def fetch_by_id(self, *, input_id: UUID) -> Item | None:
        return next((item for item in self.items if item.id == input_id), None)

    async def fetch_list(self, *, limit: int, offset: int) -> list[Item]:
        return self.items[offset : offset + limit]

    async def count(self) -> int:
        return len(self.items)

    async def create(self, *, input_dto: CreateItemDTO) -> Item:
        if any(item.title == input_dto.title for item in self.items):
            raise EntityAlreadyExistsException("Item", input_dto.title)
        now = datetime.now(UTC)
        item = Item(
            id=uuid4(),
            title=input_dto.title,
            description=input_dto.description,
            created_at=now,
            updated_at=now,
        )
        self.items.append(item)
        return item

    async def update_by_id(self, *, input_id: UUID, input_dto: UpdateItemDTO) -> Item:
        item = await self.fetch_by_id(input_id=input_id)
        if item is None:
            raise EntityNotFoundException("Item", input_id)
        updated = Item(
            id=item.id,
            title=input_dto.title if input_dto.title is not None else item.title,
            description=(
                input_dto.description
                if input_dto.description is not None
                else item.description
            ),
            created_at=item.created_at,
            updated_at=datetime.now(UTC),
        )
        self.items[self.items.index(item)] = updated
        return updated

    async def delete_by_id(self, *, input_id: UUID) -> None:
        item = await self.fetch_by_id(input_id=input_id)
        if item is None:
            raise EntityNotFoundException("Item", input_id)
        self.items.remove(item)
