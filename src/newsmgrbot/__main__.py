import asyncio
import contextlib
import datetime
import logging
import os

import dishka
import uvloop
from sqlalchemy.ext.asyncio import AsyncEngine, close_all_sessions
from telegram import BotCommand, LinkPreviewOptions, Update
from telegram.constants import ParseMode
from telegram.ext import (
    AIORateLimiter,
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Defaults,
    MessageHandler,
    TypeHandler,
    filters,
)

from newsmgrbot.callbacks.auth import auth_callback
from newsmgrbot.callbacks.help import help_callback
from newsmgrbot.callbacks.parser import parser_callback
from newsmgrbot.callbacks.sources import (
    check_source_callback,
    new_source_entry,
    new_source_feed_url,
    sources_callback,
)
from newsmgrbot.callbacks.start import start_callback
from newsmgrbot.models import Base
from newsmgrbot.provider import Provider


async def main() -> None:
    application = (
        Application.builder()
        .token(os.environ["TELEGRAM_BOT_TOKEN"])
        .defaults(
            Defaults(
                parse_mode=ParseMode.HTML,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
        )
        .rate_limiter(AIORateLimiter())
        .build()
    )

    application.add_handlers(
        {
            -1: [TypeHandler(Update, auth_callback)],
            0: [
                CommandHandler("start", start_callback),
                CommandHandler("help", help_callback),
                CommandHandler("sources", sources_callback),
                CallbackQueryHandler(check_source_callback, r"^source_"),
                ConversationHandler(
                    entry_points=[CallbackQueryHandler(new_source_entry, r"^new_source$")],
                    states={1: [MessageHandler(filters.TEXT, new_source_feed_url)]},
                    fallbacks=[],
                ),
            ],
        }
    )

    job = application.job_queue.run_repeating(
        callback=parser_callback,
        interval=datetime.timedelta(minutes=1),
    )

    container = application.bot_data["container"] = dishka.make_async_container(
        Provider(db_url=os.environ["POSTGRES_URL"])
    )

    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        await application.initialize()
        await application.bot.set_my_commands(
            commands=(
                BotCommand(command="start", description="introduction message"),
                BotCommand(command="help", description="help message"),
                BotCommand(command="sources", description="manage your sources"),
            )
        )
        await application.start()
        await application.updater.start_polling()
        await job.run(application)
        await asyncio.Event().wait()
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        await close_all_sessions()
        await container.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("httpx").setLevel(level=logging.WARNING)
    with contextlib.suppress(SystemExit, KeyboardInterrupt):
        uvloop.run(main())
