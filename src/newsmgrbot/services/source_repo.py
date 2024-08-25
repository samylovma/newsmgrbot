from collections.abc import Sequence
from datetime import UTC, datetime

from sqlalchemy import insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from newsmgrbot.models import Source


class SourceNotFoundError(Exception):
    pass


class SourceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.__session: AsyncSession = session

    async def create(self, title: str, url: str, feed_url: str) -> Source:
        return await self.__session.scalar(
            insert(Source).values(title=title, url=url, feed_url=feed_url, added_at=datetime.now(UTC)).returning(Source)
        )

    async def get(self, source_id: int) -> Source:
        try:
            return await self.__session.get_one(Source, source_id)
        except NoResultFound as e:
            raise SourceNotFoundError from e

    async def get_all(self) -> Sequence[Source]:
        return (await self.__session.scalars(select(Source))).all()
