from collections.abc import AsyncGenerator

import dishka
import edgedb
import httpx

from newsmgrbot.adapters.feed_scraper import FeedScraper
from newsmgrbot.adapters.news_repo import NewsRepository
from newsmgrbot.adapters.source_repo import SourceRepository
from newsmgrbot.adapters.user_repo import UserRepository
from newsmgrbot.config import Config


class MainProvider(dishka.Provider):
    def __init__(self, config: Config) -> None:
        super().__init__()
        self.__config: Config = config

    @dishka.provide(scope=dishka.Scope.APP)
    async def get_edgedb_client(
        self,
    ) -> AsyncGenerator[edgedb.AsyncIOClient, None]:
        client = edgedb.create_async_client(self.__config.EDGEDB_DSN)
        yield client
        await client.aclose()

    @dishka.provide(scope=dishka.Scope.APP)
    async def get_httpx_client(
        self,
    ) -> AsyncGenerator[httpx.AsyncClient, None]:
        async with httpx.AsyncClient() as client:
            yield client

    edgedb_executor = dishka.alias(
        edgedb.AsyncIOClient, provides=edgedb.AsyncIOExecutor
    )

    scraper = dishka.provide(FeedScraper, scope=dishka.Scope.REQUEST)
    user_repo = dishka.provide(UserRepository, scope=dishka.Scope.REQUEST)
    source_repo = dishka.provide(SourceRepository, scope=dishka.Scope.REQUEST)
    news_repo = dishka.provide(NewsRepository, scope=dishka.Scope.REQUEST)
