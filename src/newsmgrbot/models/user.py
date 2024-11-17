from dataclasses import dataclass

from newsmgrbot.models.telegram_id import TelegramId
from newsmgrbot.models.user_id import UserId


@dataclass
class User:
    id: UserId
    telegram_id: TelegramId
