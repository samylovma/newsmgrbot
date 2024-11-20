from collections.abc import AsyncGenerator

import dishka
import edgedb

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

    user_repo = dishka.provide(UserRepository, scope=dishka.Scope.REQUEST)
