import datetime

import dishka
from telegram import LinkPreviewOptions, Update
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


def create_app(config: Config) -> Application:
    application = (
        Application.builder()
        .token(config.TELEGRAM_BOT_TOKEN)
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
                CommandHandler("privacy", privacy_callback),
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
    application.job_queue.run_repeating(
        callback=parser_callback,
        interval=datetime.timedelta(minutes=1),
    )
    application.bot_data["container"] = dishka.make_async_container(Provider(db_url=config.DATABASE_URL))
    return application
