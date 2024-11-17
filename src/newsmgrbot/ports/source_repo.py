from collections.abc import Sequence
from typing import Protocol

from newsmgrbot.models.source import Source
from newsmgrbot.models.source_id import SourceId


class SourceRepository(Protocol):
    async def create(self, source: Source) -> None:
        raise NotImplementedError

    async def get_by_id(self, id_: SourceId) -> Source:
        raise NotImplementedError

    async def get_all(self) -> Sequence[Source]:
        raise NotImplementedError
