from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from newsmgrbot.models import News


class NewsNotFoundError(Exception):
    pass


class NewsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.__session: AsyncSession = session

    async def upsert(self, news: News) -> News:
        return await self.__session.merge(news)

    async def get(self, source_id: int, internal_id: str) -> News:
        try:
            return await self.__session.get_one(News, {"source_id": source_id, "internal_id": internal_id})
        except NoResultFound as e:
            raise NewsNotFoundError from e
