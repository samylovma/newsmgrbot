import asyncio

from dishka import FromDishka
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from newsmgrbot.di import inject
from newsmgrbot.models import News
from newsmgrbot.services.feed_scraper import FeedScraper
from newsmgrbot.services.news_repo import NewsNotFoundError, NewsRepository
from newsmgrbot.services.source_repo import SourceRepository
from newsmgrbot.services.user_repo import UserRepository


@inject
async def parser_callback(
    context: ContextTypes.DEFAULT_TYPE,
    user_repo: FromDishka[UserRepository],
    source_repo: FromDishka[SourceRepository],
    news_repo: FromDishka[NewsRepository],
    feed_scraper: FromDishka[FeedScraper],
) -> None:
    new_news: list[News] = []
    sources = await source_repo.get_all()
    feeds = await asyncio.gather(*[feed_scraper.scrap(source.feed_url) for source in sources])
    for source, feed in zip(sources, feeds, strict=True):
        for news in feed.news:
            news_model = News(
                source_id=source.id,
                internal_id=news.id,
                title=news.title,
                url=news.url,
                pub_date=news.pub_date,
                description=news.description,
            )
            try:
                await news_repo.get(source_id=source.id, internal_id=news.id)
            except NewsNotFoundError:
                if news.pub_date >= source.added_at:
                    new_news.append(news_model)
            await news_repo.upsert(news_model)

    for i in range(len(new_news)):
        for j in range(i + 1, len(new_news)):
            if new_news[i].pub_date > new_news[j].pub_date:
                new_news[i], new_news[j] = new_news[j], new_news[i]

    for news in new_news:
        source = await source_repo.get(news.source_id)
        text = f"<b>«{news.title}» — «{source.title}»</b>"
        if news.description:
            text += f"\n\n<blockquote expandable>{news.description}</blockquote>"
        users_ids = await user_repo.get_users_ids_by_source_id(news.source_id)
        for user_id in users_ids:
            context.application.create_task(
                context.bot.send_message(
                    chat_id=user_id,
                    text=text,
                    reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton(text="Link", url=news.url)),
                )
            )
