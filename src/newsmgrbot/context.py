from dataclasses import dataclass, field
from typing import Any

from dishka import AsyncContainer
from telegram.ext import AIORateLimiter, Application, CallbackContext, ExtBot

from newsmgrbot.models.user import User


@dataclass
class BotData:
    dishka_container: AsyncContainer = field(init=False)


@dataclass
class Context(
    CallbackContext[
        ExtBot[AIORateLimiter],
        dict[Any, Any],
        dict[Any, Any],
        BotData,
    ]
):
    dishka_container: AsyncContainer = field(init=False)
    user: User = field(init=False)

    def __init__(
        self,
        application: Application,  # type: ignore[type-arg]
        chat_id: int | None = None,
        user_id: int | None = None,
    ) -> None:
        super().__init__(
            application=application,
            chat_id=chat_id,
            user_id=user_id,
        )
