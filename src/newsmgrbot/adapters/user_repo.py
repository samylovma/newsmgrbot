from collections.abc import Sequence
from dataclasses import dataclass

import edgedb
import msgspec

from newsmgrbot.models.source import Source
from newsmgrbot.models.source_id import SourceId
from newsmgrbot.models.user import User
from newsmgrbot.models.user_id import UserId


class UserNotFoundError(Exception):
    pass


@dataclass
class CreateUser:
    telegram_id: int


class UserRepository:
    def __init__(self, client: edgedb.AsyncIOClient) -> None:
        self.__client = client

    async def create(self, data: CreateUser) -> User:
        result = await self.__client.query_required_single_json(
            """
            select(
                insert User { telegram_id := <int64>$telegram_id }
            ) { * }
            """,
            telegram_id=data.telegram_id,
        )
        return msgspec.json.decode(result, type=User)

    async def get_by_id(self, user_id: UserId) -> User:
        try:
            result = await self.__client.query_required_single_json(
                "select User { * } filter .id = <uuid>$user_id",
                user_id=user_id,
            )
        except edgedb.NoDataError as exc:
            raise UserNotFoundError from exc
        return msgspec.json.decode(result, type=User)

    async def get_by_telegram_id(self, telegram_id: int) -> User:
        try:
            result = await self.__client.query_required_single_json(
                "select User { * } filter .telegram_id = <int64>$telegram_id",
                telegram_id=telegram_id,
            )
        except edgedb.NoDataError as exc:
            raise UserNotFoundError from exc
        return msgspec.json.decode(result, type=User)

    async def get_subscriptions(self, user_id: UserId) -> Sequence[Source]:
        result = await self.__client.query_json(
            "select User { subscriptions: { * } } filter .id = <uuid>$user_id",
            user_id=user_id,
        )
        data = msgspec.json.decode(result)
        return [
            msgspec.convert(source, type=Source)
            for source in data["subscriptions"]
        ]

    async def add_subscription(
        self, user_id: UserId, source_id: SourceId
    ) -> None:
        await self.__client.query_required_single_json(
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

    async def remove_subscription(
        self, user_id: UserId, source_id: SourceId
    ) -> None:
        await self.__client.query_required_single_json(
            """
            update User
            filter .id = <uuid>$user_id
            set {
                subscriptions -= (
                    select Source
                    filter .id = <uuid>$source_id
                )

            }
            """,
            user_id=user_id,
            source_id=source_id,
        )
