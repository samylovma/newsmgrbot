from dataclasses import dataclass
from datetime import datetime

import edgedb
import msgspec

from newsmgrbot.models.news import News
from newsmgrbot.models.news_id import NewsId
from newsmgrbot.models.source_id import SourceId


@dataclass
class CreateNews:
    source_id: SourceId
    internal_id: str
    title: str
    url: str
    description: str | None
    publication_date: datetime


class NewsRepository:
    def __init__(self, client: edgedb.AsyncIOClient) -> None:
        self.__client = client

    async def create(self, data: CreateNews) -> News:
        result = await self.__client.query_required_single_json(
            """
            select(
                insert News {
                    source := <uuid>$source_id;
                    internal_id := <str>$internal_id;
                    title := <str>$title;
                    url := <str>$url;
                    description := <str>$description;
                    publication_date := <datetime>$publication_date;
                }
            ) { * }
            """,
            source_id=data.source_id,
            internal_id=data.internal_id,
            title=data.title,
            url=data.url,
            description=data.description,
            publication_date=data.publication_date,
        )
        return msgspec.json.decode(result, type=News)

    async def get_by_id(self, news_id: NewsId) -> News:
        result = await self.__client.query_required_single_json(
            "select News { * } filter .id = <uuid>$news_id",
            news_id=news_id,
        )
        return msgspec.json.decode(result, type=News)
