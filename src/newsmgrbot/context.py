import dataclasses
from typing import Any

import dishka
import telegram.ext


@dataclasses.dataclass(slots=True)
class BotData:
    dishka_container: dishka.AsyncContainer | None = None


class Context(
    telegram.ext.CallbackContext[
        telegram.ext.ExtBot[telegram.ext.AIORateLimiter], dict[Any, Any], dict[Any, Any], BotData
    ]
):
    def __init__(
        self,
        application: telegram.ext.Application,
        chat_id: int | None = None,
        user_id: int | None = None,
    ) -> None:
        super().__init__(
            application=application,
            chat_id=chat_id,
            user_id=user_id,
        )
        self.__dishka_container: dishka.AsyncContainer | None = None

    @property
    def dishka_container(self) -> dishka.AsyncContainer:
        if self.__dishka_container is None:
            raise RuntimeError("No container")
        return self.__dishka_container

    @dishka_container.setter
    def dishka_container(self, value: dishka.AsyncContainer) -> None:
        self.__dishka_container = value
