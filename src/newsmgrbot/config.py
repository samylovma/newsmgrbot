import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Config:
    TELEGRAM_BOT_TOKEN: str
    DATABASE_URL: str


def parse_config() -> Config:
    return Config(
        TELEGRAM_BOT_TOKEN=os.environ["TELEGRAM_BOT_TOKEN"],
        DATABASE_URL=os.environ["DATABASE_URL"],
    )
