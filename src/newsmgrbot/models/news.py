from dataclasses import dataclass
from datetime import datetime

from newsmgrbot.models.news_id import NewsId
from newsmgrbot.models.source_id import SourceId


@dataclass
class News:
    id: NewsId
    source_id: SourceId
    internal_id: str
    title: str
    description: str | None
    url: str
    pub_date: datetime
