import datetime
import email.utils
from dataclasses import dataclass

import httpx
import xmltodict


@dataclass(frozen=True, slots=True)
class News:
    id: str
    title: str
    description: str | None
    url: str
    pub_date: datetime.datetime


@dataclass(frozen=True, slots=True)
class Feed:
    title: str
    url: str
    news: list[News]


class FeedFetchError(Exception):
    pass


class FeedScraper:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.__client: httpx.AsyncClient = client

    async def scrap(self, feed_url: str) -> Feed:
        try:
            response = await self.__client.get(feed_url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise FeedFetchError from e
        rss_feed = xmltodict.parse(response.text)
        return Feed(
            title=rss_feed["rss"]["channel"]["title"],
            url=rss_feed["rss"]["channel"]["link"],
            news=[
                News(
                    id=item["guid"],
                    title=item["title"],
                    description=item.get("description"),
                    url=item["link"],
                    pub_date=email.utils.parsedate_to_datetime(item["pubDate"]),
                )
                for item in rss_feed["rss"]["channel"]["item"]
            ],
        )
