from datetime import datetime

from advanced_alchemy.base import BigIntAuditBase, orm_registry
from sqlalchemy import BigInteger, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

user_source = Table(
    "user_source",
    orm_registry.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("source_id", ForeignKey("source.id")),
)


class User(BigIntAuditBase):
    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True)

    sources: Mapped[list["Source"]] = relationship(secondary=user_source, back_populates="users", lazy="selectin")


class Source(BigIntAuditBase):
    title: Mapped[str]
    url: Mapped[str]
    feed_url: Mapped[str]

    users: Mapped[list[User]] = relationship(secondary=user_source, back_populates="sources", lazy="selectin")
    news: Mapped[list["News"]] = relationship(back_populates="source", lazy="selectin")


class News(BigIntAuditBase):
    source_id: Mapped[int] = mapped_column(ForeignKey(Source.id), index=True)
    internal_id: Mapped[str] = mapped_column(index=True)
    title: Mapped[str]
    description: Mapped[str | None]
    url: Mapped[str]
    pub_date: Mapped[datetime]

    source: Mapped[Source] = relationship(back_populates="news", lazy="selectin")
