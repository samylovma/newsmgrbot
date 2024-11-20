import email.utils
from dataclasses import dataclass
from datetime import datetime

import httpx
import xmltodict


class ScrapError(Exception):
    pass


@dataclass
class FeedNews:
    internal_id: str
    title: str
    url: str
    description: str | None
    publication_date: datetime


@dataclass
class Feed:
    title: str
    url: str
    description: str | None
    news: list[FeedNews]


class FeedScraper:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.__client = client

    async def scrap(self, feed_url: str) -> Feed:
        response = await self.__client.get(feed_url)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ScrapError from exc
        data = xmltodict.parse(
            xml_input=response.text, encoding=response.encoding
        )
        channel = data["rss"]["channel"]
        return Feed(
            title=channel["title"],
            url=channel["link"],
            description=channel.get("description"),
            news=[
                FeedNews(
                    internal_id=item["guid"],
                    title=item["title"],
                    url=item["link"],
                    description=item["description"],
                    publication_date=email.utils.parsedate_to_datetime(
                        item["pubDate"]
                    ),
                )
                for item in channel["item"]
            ],
        )
