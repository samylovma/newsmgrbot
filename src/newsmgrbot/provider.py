from collections.abc import AsyncIterable

import dishka
import httpx
import sqlalchemy.ext.asyncio as sa

from newsmgrbot.services.news import NewsService
from newsmgrbot.services.scraper import FeedScraper
from newsmgrbot.services.source import SourceService
from newsmgrbot.services.user import UserService


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
        async with sa_sessionmaker() as session:
            yield session

    @dishka.provide(scope=dishka.Scope.APP)
    async def provide_httpx_client(self) -> AsyncIterable[httpx.AsyncClient]:
        async with httpx.AsyncClient() as client:
            yield client

    @dishka.provide(scope=dishka.Scope.REQUEST)
    async def provide_user_service(self, sa_session: sa.AsyncSession) -> UserService:
        return UserService(session=sa_session, auto_commit=True)

    @dishka.provide(scope=dishka.Scope.REQUEST)
    async def provide_source_service(self, sa_session: sa.AsyncSession) -> SourceService:
        return SourceService(session=sa_session, auto_commit=True)

    @dishka.provide(scope=dishka.Scope.REQUEST)
    async def provide_news_service(self, sa_session: sa.AsyncSession) -> NewsService:
        return NewsService(session=sa_session, auto_commit=True)

    feed_scraper = dishka.provide(FeedScraper, scope=dishka.Scope.REQUEST)
