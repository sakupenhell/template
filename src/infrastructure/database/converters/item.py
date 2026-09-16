from typing import Any

from sqlalchemy import Row

from src.domain.entities.item import Item


def convert_row_to_item(row: Row[Any]) -> Item:
    return Item(
        id=row.id,
        title=row.title,
        description=row.description,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )
