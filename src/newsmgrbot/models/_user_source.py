from typing import Final

from advanced_alchemy.base import orm_registry
from sqlalchemy import Column, ForeignKey, Table

user_source: Final = Table(
    "user_source",
    orm_registry.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("source_id", ForeignKey("source.id")),
)
