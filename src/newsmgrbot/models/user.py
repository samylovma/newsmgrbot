from dataclasses import dataclass
from datetime import datetime

from newsmgrbot.models.user_id import UserId


@dataclass
class User:
    id: UserId
    telegram_id: int
    created_at: datetime
    updated_at: datetime
