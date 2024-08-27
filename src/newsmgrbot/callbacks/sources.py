import logging
from collections.abc import Iterable

from dishka import FromDishka
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes, ConversationHandler

from newsmgrbot.di import inject
from newsmgrbot.models import Source
from newsmgrbot.services.scraper import FeedFetchError, FeedScraper
from newsmgrbot.services.source import SourceService
from newsmgrbot.services.user import UserService

_logger = logging.getLogger(__name__)


_SOURCES_MENU_TEXT = """<b>Sources</b>

☑️ means that source added to yours.

To add source click on it."""


@inject
async def sources_callback(
    update: Update,
    _: ContextTypes.DEFAULT_TYPE,
    user_service: FromDishka[UserService],
    source_service: FromDishka[SourceService],
) -> None:
    all_sources = await source_service.list()
    user = await user_service.get_one(tg_id=update.message.from_user.id)
    await update.message.reply_text(
        text=_SOURCES_MENU_TEXT,
        reply_markup=_get_sources_keyboard(all_sources=all_sources, user_sources=user.sources),
        reply_to_message_id=update.message.id,
    )


@inject
async def check_source_callback(
    update: Update,
    _: ContextTypes.DEFAULT_TYPE,
    user_service: FromDishka[UserService],
    source_service: FromDishka[SourceService],
) -> None:
    source_id = int(update.callback_query.data.split("_")[1])
    user = await user_service.get_one(tg_id=update.effective_user.id)
    source = await source_service.get(source_id)
    if source in user.sources:
        user.sources.remove(source)
        user = await user_service.upsert(user)
        await update.callback_query.answer("The source has been successfully removed.")
    else:
        user.sources.append(source)
        user = await user_service.upsert(user)
        await update.callback_query.answer("The source has been successfully added.")

    all_sources = await source_service.list()
    await update.callback_query.edit_message_reply_markup(
        _get_sources_keyboard(all_sources=all_sources, user_sources=user.sources)
    )


async def new_source_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please send feed url.",
        reply_markup=ForceReply(),
        reply_to_message_id=(
            update.callback_query.message.message_id if update.callback_query.message.is_accessible else None
        ),
    )
    return 1


@inject
async def new_source_feed_url(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_service: FromDishka[UserService],
    source_service: FromDishka[SourceService],
    feed_scraper: FromDishka[FeedScraper],
) -> int:
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    user = await user_service.get_one(tg_id=update.effective_user.id)
    all_sources = await source_service.list()
    try:
        feed = await feed_scraper.scrap(update.message.text)
    except FeedFetchError as exc:
        _logger.exception("Error while fetching feed: %s", update.message.text, exc_info=exc)
        await update.message.reply_text(
            text="Sorry, I can't fetch feed from URL. Please try again later.",
            reply_to_message_id=update.message.id,
        )
        await update.message.reply_text(
            text=_SOURCES_MENU_TEXT,
            reply_markup=_get_sources_keyboard(all_sources=all_sources, user_sources=user.sources),
        )
        return ConversationHandler.END
    source = await source_service.create({"title": feed.title, "url": feed.url, "feed_url": update.message.text})
    user.sources.append(source)
    user = await user_service.upsert(user)
    all_sources = await source_service.list()
    await update.message.reply_text(
        text="Successfully created!",
        reply_to_message_id=update.message.id,
    )
    await update.message.reply_text(
        text=_SOURCES_MENU_TEXT,
        reply_markup=_get_sources_keyboard(all_sources=all_sources, user_sources=user.sources),
    )
    return ConversationHandler.END


def _get_sources_keyboard(all_sources: Iterable[Source], user_sources: Iterable[Source]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup.from_column(
        [
            *[
                InlineKeyboardButton(
                    text=f"{"☑️ " if source in user_sources else ""}{source.title}",
                    callback_data=f"source_{source.id}",
                )
                for source in all_sources
            ],
            InlineKeyboardButton(text="➕ New source", callback_data="new_source"),  # noqa: RUF001
        ]
    )
