from collections.abc import AsyncIterable

import dishka
import httpx
import sqlalchemy.ext.asyncio as sa

from newsmgrbot.services.feed_scraper import FeedScraper
from newsmgrbot.services.news_repo import NewsRepository
from newsmgrbot.services.source_repo import SourceRepository
from newsmgrbot.services.user_repo import UserRepository


class Provider(dishka.Provider):
    def __init__(self, db_url: str) -> None:
        super().__init__()
        self.db_url = db_url

    @dishka.provide(scope=dishka.Scope.APP)
    async def provide_sa_engine(self) -> sa.AsyncEngine:
        return sa.create_async_engine(self.db_url)

    @dishka.provide(scope=dishka.Scope.APP)
    async def provide_sa_sessionmaker(self, sa_engine: sa.AsyncEngine) -> sa.async_sessionmaker[sa.AsyncSession]:
        return sa.async_sessionmaker(bind=sa_engine, expire_on_commit=False)

    @dishka.provide(scope=dishka.Scope.REQUEST)
    async def provide_sa_session(
        self, sa_sessionmaker: sa.async_sessionmaker[sa.AsyncSession]
    ) -> AsyncIterable[sa.AsyncSession]:
        async with sa_sessionmaker.begin() as session:
            yield session

    @dishka.provide(scope=dishka.Scope.REQUEST)
    async def provide_httpx_client(self) -> AsyncIterable[httpx.AsyncClient]:
        async with httpx.AsyncClient() as client:
            yield client

    user_repo = dishka.provide(UserRepository, scope=dishka.Scope.REQUEST)
    source_repo = dishka.provide(SourceRepository, scope=dishka.Scope.REQUEST)
    news_repo = dishka.provide(NewsRepository, scope=dishka.Scope.REQUEST)
    feed_scraper = dishka.provide(FeedScraper, scope=dishka.Scope.REQUEST)
