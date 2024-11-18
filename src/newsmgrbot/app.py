from typing import Any, cast

from dishka import make_async_container
from telegram import BotCommand, LinkPreviewOptions
from telegram.constants import ParseMode
from telegram.ext import (
    AIORateLimiter,
    Application,
    ContextTypes,
    Defaults,
    ExtBot,
    JobQueue,
)

from newsmgrbot.config import Config
from newsmgrbot.context import BotData, Context
from newsmgrbot.controllers.telegram_bot.help import HelpHandler
from newsmgrbot.controllers.telegram_bot.privacy import PrivacyHandler
from newsmgrbot.controllers.telegram_bot.start import StartHandler
from newsmgrbot.ioc import MainProvider

type _Application = Application[
    ExtBot[AIORateLimiter],
    Context,
    dict[Any, Any],
    dict[Any, Any],
    BotData,
    JobQueue[Context],
]


def create_app(config: Config) -> _Application:
    app = cast(
        _Application,
        (
            Application.builder()
            .token(config.TELEGRAM_BOT_TOKEN)
            .defaults(
                Defaults(
                    parse_mode=ParseMode.HTML,
                    link_preview_options=LinkPreviewOptions(is_disabled=True),
                )
            )
            .post_init(_post_init)
            .post_shutdown(_post_shutdown)
            .rate_limiter(AIORateLimiter())
            .context_types(ContextTypes(context=Context, bot_data=BotData))
            .build()
        ),
    )
    app.add_handlers(
        (
            StartHandler(),
            HelpHandler(),
            PrivacyHandler(),
        )
    )
    app.bot_data.dishka_container = make_async_container(
        MainProvider(config=config)
    )
    return app


async def _post_init(application: _Application) -> None:
    await application.bot.set_my_commands(
        commands=(
            BotCommand(command="start", description="introduction message"),
            BotCommand(command="help", description="help message"),
            BotCommand(command="privacy", description="privacy policy"),
            BotCommand(command="sources", description="manage your sources"),
        )
    )


async def _post_shutdown(application: _Application) -> None:
    if dishka_container := application.bot_data.dishka_container:
        await dishka_container.close()
