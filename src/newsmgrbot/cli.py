import logging

import click

from newsmgrbot.app import create_app
from newsmgrbot.config import parse_config


@click.group()
def cli() -> None:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("httpx").setLevel(level=logging.WARNING)
    logging.getLogger("apscheduler").setLevel(level=logging.WARNING)


@cli.command()
def run_polling() -> None:
    config = parse_config()
    app = create_app(config)
    app.run_polling()


@cli.command()
def run_webhook() -> None:
    config = parse_config()
    app = create_app(config)
    app.run_webhook()


if __name__ == "__main__":
    cli()
