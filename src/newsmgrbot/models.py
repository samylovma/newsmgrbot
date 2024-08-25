import datetime
from typing import ClassVar

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
)


class Base(MappedAsDataclass, DeclarativeBase, unsafe_hash=True):
    type_annotation_map: ClassVar = {
        int: BigInteger,
        str: Text,
    }


user_to_source = Table(
    "user_to_source",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("source_id", ForeignKey("source.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)


class Source(Base):
    __tablename__ = "source"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    url: Mapped[str]
    feed_url: Mapped[str]
    added_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )


class News(Base):
    __tablename__ = "news"

    source_id: Mapped[int] = mapped_column(ForeignKey(Source.id), primary_key=True)
    internal_id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    url: Mapped[str]
    pub_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    description: Mapped[str | None] = mapped_column(default=None)
