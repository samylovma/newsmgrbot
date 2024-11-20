import functools
from collections.abc import Awaitable, Callable

from telegram import Update

from newsmgrbot.adapters.user_repo import (
    CreateUser,
    UserNotFoundError,
    UserRepository,
)
from newsmgrbot.context import Context


def auth[R](
    func: Callable[[Update, Context], Awaitable[R]],
) -> Callable[[Update, Context], Awaitable[R]]:
    @functools.wraps(func)
    async def wrapper(update: Update, context: Context) -> R:
        tg_user = update.effective_user
        if tg_user is None:
            raise RuntimeError("No user in update")
        user_repo = await context.dishka_container.get(UserRepository)
        try:
            user = await user_repo.get_by_telegram_id(tg_user.id)
        except UserNotFoundError:
            user = await user_repo.create(CreateUser(telegram_id=tg_user.id))
        context.user = user
        return await func(update, context)

    return wrapper
