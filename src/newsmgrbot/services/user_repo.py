from sqlalchemy import delete, insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from newsmgrbot.models import User, user_to_source


class UserNotFoundError(Exception):
    pass


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.__session: AsyncSession = session

    async def upsert(self, user: User) -> User:
        return await self.__session.merge(user)

    async def get(self, user_id: int) -> User:
        try:
            return await self.__session.get_one(User, user_id)
        except NoResultFound as e:
            raise UserNotFoundError from e

    async def add_source(self, user_id: int, source_id: int) -> None:
        await self.__session.execute(insert(user_to_source).values(user_id=user_id, source_id=source_id))

    async def get_sources_ids(self, user_id: int) -> list[int]:
        return [
            row[1]
            for row in await self.__session.execute(select(user_to_source).where(user_to_source.c.user_id == user_id))
        ]

    async def remove_source(self, user_id: int, source_id: int) -> None:
        await self.__session.execute(
            delete(user_to_source).where(
                (user_to_source.c.user_id == user_id) & (user_to_source.c.source_id == source_id)
            )
        )

    async def get_users_ids_by_source_id(self, source_id: int) -> list[int]:
        return [
            row[0]
            for row in await self.__session.execute(
                select(user_to_source).where(user_to_source.c.source_id == source_id)
            )
        ]
