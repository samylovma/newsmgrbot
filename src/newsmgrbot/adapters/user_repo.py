from typing import cast

import edgedb

from newsmgrbot.models.source_id import SourceId
from newsmgrbot.models.user import User
from newsmgrbot.models.user_id import UserId


class UserNotFoundError(Exception):
    pass


class UserRepository:
    def __init__(self, client: edgedb.AsyncIOExecutor) -> None:
        self.__client = client

    async def create(self, telegram_id: int) -> User:
        return cast(
            User,
            await self.__client.query_required_single(
                """
                select(
                    insert User { telegram_id := <int64>$telegram_id }
                ) { * }
                """,
                telegram_id=telegram_id,
            ),
        )

    async def get_by_id(self, user_id: UserId) -> User:
        try:
            return cast(
                User,
                await self.__client.query_required_single(
                    """
                    select User { * }
                    filter .id = <uuid>$user_id
                    """,
                    user_id=user_id,
                ),
            )
        except edgedb.NoDataError as exc:
            raise UserNotFoundError from exc

    async def get_by_telegram_id(self, telegram_id: int) -> User:
        try:
            return cast(
                User,
                await self.__client.query_required_single(
                    """
                    select User { * }
                    filter .telegram_id = <int64>$telegram_id
                    """,
                    telegram_id=telegram_id,
                ),
            )
        except edgedb.NoDataError as exc:
            raise UserNotFoundError from exc

    async def add_subscription(
        self, user_id: UserId, source_id: SourceId
    ) -> None:
        await self.__client.query_required_single(
            """
            update User
            filter .id = <uuid>$user_id
            set {
                subscriptions += (
                    select Source
                    filter .id = <uuid>$source_id
                )
            }
            """,
            user_id=user_id,
            source_id=source_id,
        )
