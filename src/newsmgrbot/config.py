import os
from dataclasses import dataclass

import dotenv


@dataclass(frozen=True, kw_only=True, slots=True)
class Config:
    TELEGRAM_BOT_TOKEN: str
    EDGEDB_DSN: str


def parse_config() -> Config:
    dotenv.load_dotenv()
    return Config(
        TELEGRAM_BOT_TOKEN=os.environ["TELEGRAM_BOT_TOKEN"],
        EDGEDB_DSN=os.environ["EDGEDB_DSN"],
    )
