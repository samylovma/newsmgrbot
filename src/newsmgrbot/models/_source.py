from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from ._news import News
    from ._user import User


class Source(BigIntAuditBase):
    title: Mapped[str]
    url: Mapped[str]
    feed_url: Mapped[str]

    users: Mapped[list["User"]] = relationship(secondary="user_source", back_populates="sources", lazy="selectin")
    news: Mapped[list["News"]] = relationship(back_populates="source", lazy="selectin")
