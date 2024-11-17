from collections.abc import Sequence
from typing import Protocol

from newsmgrbot.models.source import Source
from newsmgrbot.models.source_id import SourceId
from newsmgrbot.models.telegram_id import TelegramId
from newsmgrbot.models.user import User
from newsmgrbot.models.user_id import UserId


class UserRepository(Protocol):
    async def create(self, user: User) -> None:
        raise NotImplementedError

    async def get_by_id(self, user_id: UserId) -> User:
        raise NotImplementedError

    async def get_by_telegram_id(self, telegram_id: TelegramId) -> User:
        raise NotImplementedError

    async def get_sources(self) -> Sequence[Source]:
        raise NotImplementedError

    async def add_source(self, source_id: SourceId) -> None:
        raise NotImplementedError

    async def remove_source(self, source_id: SourceId) -> None:
        raise NotImplementedError
