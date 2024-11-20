from dishka import FromDishka
from telegram import ForceReply, Message, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from newsmgrbot.adapters.feed_scraper import FeedScraper
from newsmgrbot.adapters.source_repo import CreateSource, SourceRepository
from newsmgrbot.adapters.user_repo import UserRepository
from newsmgrbot.auth import auth
from newsmgrbot.context import Context
from newsmgrbot.di import inject
from newsmgrbot.utils import message


class NewSourceCommandHandler(ConversationHandler):
    def __init__(self) -> None:
        super().__init__(
            entry_points=[CommandHandler("newsource", entry_point)],
            states={1: [MessageHandler(filters.TEXT, callback)]},
            fallbacks=[],
        )


@message
async def entry_point(message: Message, _: Context) -> int:
    await message.reply_text(
        "Please send a feed url of a source.",
        reply_markup=ForceReply(),
        reply_to_message_id=message.id,
    )
    return 1


@message
@inject
@auth
async def callback(
    message: Message,
    context: Context,
    scraper: FromDishka[FeedScraper],
    source_repo: FromDishka[SourceRepository],
    user_repo: FromDishka[UserRepository],
) -> int:
    feed_url = message.text
    feed = await scraper.scrap(feed_url)
    source = await source_repo.create(
        CreateSource(
            title=feed.title,
            url=feed.url,
            feed_url=feed_url,
            health=True,
        )
    )
    await user_repo.add_subscription(context.user.id, source.id)
    await message.reply_text(
        "Done!",
        reply_markup=ReplyKeyboardRemove(),
        reply_to_message_id=message.id,
    )
    return ConversationHandler.END
