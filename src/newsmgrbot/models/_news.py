from datetime import datetime
from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from ._source import Source


class News(BigIntAuditBase):
    source_id: Mapped[int] = mapped_column(ForeignKey("source.id"), index=True)
    internal_id: Mapped[str] = mapped_column(index=True)
    title: Mapped[str]
    description: Mapped[str | None]
    url: Mapped[str]
    pub_date: Mapped[datetime]

    source: Mapped["Source"] = relationship(back_populates="news", lazy="selectin")
