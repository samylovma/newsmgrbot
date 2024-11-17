from collections.abc import Iterable, Sequence
from typing import Protocol

from newsmgrbot.models.news import News
from newsmgrbot.models.news_id import NewsId
from newsmgrbot.models.source import Source
from newsmgrbot.models.source_id import SourceId


class NewsRepository(Protocol):
    async def create(self, news: News) -> None:
        raise NotImplementedError

    async def create_many(self, news: Iterable[News]) -> None:
        raise NotImplementedError

    async def get_by_id(self, id_: NewsId) -> Source:
        raise NotImplementedError

    async def get_by_source_id(
        self, source_id: SourceId
    ) -> Sequence[SourceId]:
        raise NotImplementedError
