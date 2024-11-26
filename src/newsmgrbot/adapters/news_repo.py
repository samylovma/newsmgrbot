from datetime import datetime
from typing import cast

import edgedb

from newsmgrbot.models.news import News
from newsmgrbot.models.news_id import NewsId
from newsmgrbot.models.source_id import SourceId


class NewsRepository:
    def __init__(self, client: edgedb.AsyncIOClient) -> None:
        self.__client = client

    async def create(  # noqa: PLR0913
        self,
        *,
        source_id: SourceId,
        internal_id: str,
        title: str,
        url: str,
        description: str | None,
        publication_date: datetime,
    ) -> News:
        return cast(
            News,
            await self.__client.query_required_single_json(
                """
                select(
                    insert News {
                        source := <uuid>$source_id,
                        internal_id := <str>$internal_id,
                        title := <str>$title,
                        url := <str>$url,
                        description := <str>$description,
                        publication_date := <datetime>$publication_date,
                    }
                ) { * }
                """,
                source_id=source_id,
                internal_id=internal_id,
                title=title,
                url=url,
                description=description,
                publication_date=publication_date,
            ),
        )

    async def get_by_id(self, news_id: NewsId) -> News:
        return cast(
            News,
            await self.__client.query_required_single_json(
                "select News { * } filter .id = <uuid>$news_id",
                news_id=news_id,
            ),
        )
