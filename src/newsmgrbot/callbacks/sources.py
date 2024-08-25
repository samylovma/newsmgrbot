import logging
from collections.abc import Iterable

from dishka import FromDishka
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes, ConversationHandler

from newsmgrbot.di import inject
from newsmgrbot.models import Source
from newsmgrbot.services.feed_scraper import FeedFetchError, FeedScraper
from newsmgrbot.services.source_repo import SourceRepository
from newsmgrbot.services.user_repo import UserRepository

_logger = logging.getLogger(__name__)


@inject
async def sources_callback(
    update: Update,
    _: ContextTypes.DEFAULT_TYPE,
    user_repo: FromDishka[UserRepository],
    source_repo: FromDishka[SourceRepository],
) -> None:
    all_sources = await source_repo.get_all()
    user_sources = await user_repo.get_sources_ids(update.effective_user.id)
    await update.message.reply_text(
        text="<b>Your sources</b>",
        reply_markup=_get_sources_keyboard(all_sources=all_sources, user_sources=user_sources),
        reply_to_message_id=update.message.id,
    )


@inject
async def check_source_callback(
    update: Update,
    _: ContextTypes.DEFAULT_TYPE,
    user_repo: FromDishka[UserRepository],
    source_repo: FromDishka[SourceRepository],
) -> None:
    source_id = int(update.callback_query.data.split("_")[1])
    user_sources = await user_repo.get_sources_ids(update.effective_user.id)
    if source_id in user_sources:
        await user_repo.remove_source(user_id=update.effective_user.id, source_id=source_id)
        await update.callback_query.answer("The source has been successfully removed.")
    else:
        await user_repo.add_source(user_id=update.effective_user.id, source_id=source_id)
        await update.callback_query.answer("The source has been successfully added.")

    all_sources = await source_repo.get_all()
    user_sources = await user_repo.get_sources_ids(user_id=update.effective_user.id)
    await update.callback_query.edit_message_reply_markup(
        _get_sources_keyboard(all_sources=all_sources, user_sources=user_sources)
    )


async def new_source_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please send feed url.",
        reply_to_message_id=(
            update.callback_query.message.message_id if update.callback_query.message.is_accessible else None
        ),
    )
    return 1


@inject
async def new_source_feed_url(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_repo: FromDishka[UserRepository],
    source_repo: FromDishka[SourceRepository],
    feed_scraper: FromDishka[FeedScraper],
) -> int | None:
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    try:
        feed = await feed_scraper.scrap(update.message.text)
    except FeedFetchError as exc:
        _logger.exception("Error while fetching feed: %s", update.message.text, exc_info=exc)
        await update.message.reply_text(
            text="Sorry, I can't fetch feed from URL. Please try again later.",
            reply_to_message_id=update.message.id,
        )
        return 1
    source = await source_repo.create(title=feed.title, url=feed.url, feed_url=update.message.text)
    await user_repo.add_source(update.effective_user.id, source.id)
    await update.message.reply_text(
        text="Successfully created!",
        reply_to_message_id=update.message.id,
    )
    all_sources = await source_repo.get_all()
    user_sources = await user_repo.get_sources_ids(update.effective_user.id)
    await update.message.reply_text(
        text="<b>Your sources</b>",
        reply_markup=_get_sources_keyboard(all_sources=all_sources, user_sources=user_sources),
    )
    return ConversationHandler.END


def _get_sources_keyboard(all_sources: Iterable[Source], user_sources: Iterable[int]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup.from_column(
        [
            *[
                InlineKeyboardButton(
                    text=f"{"✅ " if source.id in user_sources else ""}{source.title}",
                    callback_data=f"source_{source.id}",
                )
                for source in all_sources
            ],
            InlineKeyboardButton(text="➕ New source", callback_data="new_source"),  # noqa: RUF001
        ]
    )
