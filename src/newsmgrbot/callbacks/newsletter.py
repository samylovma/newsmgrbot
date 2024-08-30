import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

from dishka import FromDishka
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from newsmgrbot.di import inject
from newsmgrbot.services.news import NewsService
from newsmgrbot.services.scraper import FeedScraper
from newsmgrbot.services.source import SourceService

_logger = logging.getLogger(__name__)


@inject
async def newsletter_callback(
    context: ContextTypes.DEFAULT_TYPE,
    source_service: FromDishka[SourceService],
    news_service: FromDishka[NewsService],
    feed_scraper: FromDishka[FeedScraper],
) -> None:
    news_data_list: list[dict[str, Any]] = []
    sources = await source_service.list()
    feeds = await asyncio.gather(*[feed_scraper.scrap(source.feed_url) for source in sources], return_exceptions=True)
    for source, feed in zip(sources, feeds, strict=True):
        if isinstance(feed, BaseException):
            _logger.error("Ignoring the exception while scraping the source with ID %s.", source.id, exc_info=feed)
            continue
        for feed_news in feed.news:
            if (
                feed_news.pub_date >= source.created_at
                and feed_news.pub_date <= datetime.now(UTC)
                and not await news_service.exists(source_id=source.id, internal_id=feed_news.id)
            ):
                news_data_list.append(  # noqa: PERF401
                    {
                        "source_id": source.id,
                        "internal_id": feed_news.id,
                        "title": feed_news.title,
                        "url": feed_news.url,
                        "pub_date": feed_news.pub_date,
                        "description": feed_news.description,
                    }
                )
    news_list = await news_service.create_many(news_data_list)
    news_list = sorted(news_list, key=lambda news: news.pub_date)
    for news in news_list:
        text = f"<b>{news.title} — {news.source.title}</b>"
        if news.description:
            text += f"\n\n<blockquote expandable>{news.description}</blockquote>"
        for user in news.source.users:
            await context.bot.send_message(
                chat_id=user.tg_id,
                text=text,
                reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton(text="Link", url=news.url)),
            )
