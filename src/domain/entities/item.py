from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class Item:
    id: UUID
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime
