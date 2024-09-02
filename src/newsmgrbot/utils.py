import functools
from collections.abc import Callable
from typing import cast

from telegram import Message, Update

from newsmgrbot.context import Context


def message[R](func: Callable[[Message, Context], R]) -> Callable[[Update, Context], R]:
    @functools.wraps(func)
    def wrapper(update: Update, context: Context) -> R:
        message = cast(Message, update.message)
        return func(message, context)

    return wrapper
