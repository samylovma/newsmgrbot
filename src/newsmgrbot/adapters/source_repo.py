from collections.abc import Sequence
from dataclasses import dataclass
from typing import cast

import edgedb
import msgspec

from newsmgrbot.models.source import Source
from newsmgrbot.models.source_id import SourceId


class SourceNotFoundError(Exception):
    pass


@dataclass
class CreateSource:
    title: str
    url: str
    feed_url: str
    health: bool


class SourceRepository:
    def __init__(self, client: edgedb.AsyncIOClient) -> None:
        self.__client = client

    async def create(self, data: CreateSource) -> Source:
        result = await self.__client.query_required_single_json(
            """
            select(
                insert Source {
                    title := <str>$title,
                    url := <str>$url,
                    feed_url := <str>$feed_url,
                    health := <bool>$health
                }
            ) { * }
            """,
            title=data.title,
            url=data.url,
            feed_url=data.feed_url,
            health=data.health,
        )
        return msgspec.json.decode(result, type=Source)

    async def get_by_id(self, source_id: SourceId) -> Source:
        try:
            result = await self.__client.query_required_single_json(
                "select Source { * } filter .id=<uuid>$source_id",
                source_id=source_id,
            )
        except edgedb.NoDataError as exc:
            raise SourceNotFoundError from exc
        return msgspec.json.decode(result, type=Source)

    async def get_all(self) -> Sequence[Source]:
        result = await self.__client.query_json(
            "select Source { * }",
        )
        return cast(Sequence[Source], msgspec.json.decode(result, type=Source))
