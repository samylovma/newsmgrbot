import asyncio
from typing import TYPE_CHECKING

from dishka import FromDishka
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from newsmgrbot.di import inject
from newsmgrbot.services.news import NewsService
from newsmgrbot.services.scraper import FeedScraper
from newsmgrbot.services.source import SourceService

if TYPE_CHECKING:
    from newsmgrbot.models.news import News


@inject
async def parser_callback(
    context: ContextTypes.DEFAULT_TYPE,
    source_service: FromDishka[SourceService],
    news_service: FromDishka[NewsService],
    feed_scraper: FromDishka[FeedScraper],
) -> None:
    new_news: list[News] = []
    sources = await source_service.list()
    feeds = await asyncio.gather(*[feed_scraper.scrap(source.feed_url) for source in sources])
    for source, feed in zip(sources, feeds, strict=True):
        for news in feed.news:
            is_exists = await news_service.exists(source_id=source.id, internal_id=news.id)
            if not is_exists and news.pub_date >= source.created_at:
                db_news = await news_service.create(
                    {
                        "source_id": source.id,
                        "internal_id": news.id,
                        "title": news.title,
                        "url": news.url,
                        "pub_date": news.pub_date,
                        "description": news.description,
                    }
                )
                new_news.append(db_news)

    for i in range(len(new_news)):
        for j in range(i + 1, len(new_news)):
            if new_news[i].pub_date > new_news[j].pub_date:
                new_news[i], new_news[j] = new_news[j], new_news[i]

    for news in new_news:
        source = await source_service.get(news.source_id)
        text = f"<b>«{news.title}» — «{source.title}»</b>"
        if news.description:
            text += f"\n\n<blockquote expandable>{news.description}</blockquote>"
        for user_id in source.users:
            context.application.create_task(
                context.bot.send_message(
                    chat_id=user_id,
                    text=text,
                    reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton(text="Link", url=news.url)),
                )
            )
