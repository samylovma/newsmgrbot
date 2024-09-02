from dataclasses import dataclass, field
from typing import Any

import dishka
import telegram.ext


@dataclass(slots=True)
class BotData:
    dishka_container: dishka.AsyncContainer = field(init=False)


@dataclass()
class Context(
    telegram.ext.CallbackContext[
        telegram.ext.ExtBot[telegram.ext.AIORateLimiter], dict[Any, Any], dict[Any, Any], BotData
    ]
):
    dishka_container: dishka.AsyncContainer = field(init=False)

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
