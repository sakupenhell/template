import uuid

from sqlalchemy import Column, DateTime, String, Table, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.database.metadata import metadata

items_table = Table(
    "items",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String(255), nullable=False),
    Column("description", String(2000), nullable=True),
    Column(
        "created_at", DateTime(timezone=True), nullable=False, server_default=func.now()
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
    UniqueConstraint("title"),
)
