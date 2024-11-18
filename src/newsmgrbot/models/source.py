from dataclasses import dataclass
from datetime import datetime

from newsmgrbot.models.source_id import SourceId


@dataclass
class Source:
    id: SourceId
    title: str
    url: str
    feed_url: str
    health: bool
    created_at: datetime
