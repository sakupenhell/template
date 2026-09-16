from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateItemDTO:
    title: str
    description: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateItemDTO:
    item_id: UUID
    title: str | None = None
    description: str | None = None
