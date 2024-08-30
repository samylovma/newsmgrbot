import datetime
from typing import Any, cast

import dishka
from telegram import BotCommand, LinkPreviewOptions, Update
from telegram.constants import ParseMode
from telegram.ext import (
    AIORateLimiter,
    Application,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Defaults,
    ExtBot,
    JobQueue,
    MessageHandler,
    TypeHandler,
    filters,
)

from newsmgrbot.callbacks.auth import auth_callback
from newsmgrbot.callbacks.help import help_callback
from newsmgrbot.callbacks.parser import parser_callback
from newsmgrbot.callbacks.privacy import privacy_callback
from newsmgrbot.callbacks.sources import (
    check_source_callback,
    new_source_entry,
    new_source_feed_url,
    sources_callback,
)
from newsmgrbot.callbacks.start import start_callback
from newsmgrbot.config import Config
from newsmgrbot.provider import Provider

type _Application = Application[
    ExtBot[AIORateLimiter],
    CallbackContext[ExtBot[AIORateLimiter], dict[Any, Any], dict[Any, Any], dict[Any, Any]],
    dict[Any, Any],
    dict[Any, Any],
    dict[Any, Any],
    JobQueue[CallbackContext[ExtBot[AIORateLimiter], dict[Any, Any], dict[Any, Any], dict[Any, Any]]],
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
            .build()
        ),
    )
    app.add_handlers(
        {
            -1: [TypeHandler(Update, auth_callback)],
            0: [
                CommandHandler("start", start_callback),  # type: ignore[arg-type]
                CommandHandler("help", help_callback),  # type: ignore[arg-type]
                CommandHandler("privacy", privacy_callback),  # type: ignore[arg-type]
                CommandHandler("sources", sources_callback),
                CallbackQueryHandler(check_source_callback, r"^source_"),
                ConversationHandler(
                    entry_points=[
                        CallbackQueryHandler(new_source_entry, r"^new_source$"),  # type: ignore[arg-type]
                    ],
                    states={1: [MessageHandler(filters.TEXT, new_source_feed_url)]},
                    fallbacks=[],
                ),
            ],
        }
    )
    app.job_queue.run_repeating(  # type: ignore[union-attr]
        callback=parser_callback,
        interval=datetime.timedelta(minutes=1),
        name="newsletter",
    )
    app.bot_data["container"] = dishka.make_async_container(Provider(db_url=config.DATABASE_URL))
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
    newsletter_job = application.job_queue.get_jobs_by_name("newsletter")[0]
    await newsletter_job.run(application)


async def _post_shutdown(application: _Application) -> None:
    container: dishka.AsyncContainer = application.bot_data["container"]
    await container.close()
