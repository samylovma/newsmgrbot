from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from newsmgrbot.models.source import Source


class User(BigIntAuditBase):
    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True)

    sources: Mapped[list["Source"]] = relationship(secondary="user_source", back_populates="users", lazy="selectin")
