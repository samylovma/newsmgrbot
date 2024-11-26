from typing import cast

import edgedb

from newsmgrbot.models.source import Source
from newsmgrbot.models.source_id import SourceId


class SourceNotFoundError(Exception):
    pass


class SourceRepository:
    def __init__(self, client: edgedb.AsyncIOExecutor) -> None:
        self.__client = client

    async def create(
        self, *, title: str, url: str, feed_url: str, health: bool
    ) -> Source:
        return cast(
            Source,
            await self.__client.query_required_single(
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
                title=title,
                url=url,
                feed_url=feed_url,
                health=health,
            ),
        )

    async def get_by_id(self, source_id: SourceId) -> Source:
        try:
            return cast(
                Source,
                await self.__client.query_required_single(
                    "select Source { * } filter .id=<uuid>$source_id",
                    source_id=source_id,
                ),
            )
        except edgedb.NoDataError as exc:
            raise SourceNotFoundError from exc
