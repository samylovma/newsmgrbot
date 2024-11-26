import functools
import itertools
from collections.abc import Awaitable, Callable

from newsmgrbot.adapters.user_repo import UserNotFoundError, UserRepository
from newsmgrbot.context import Context


def auth[**P, R](
    func: Callable[P, Awaitable[R]],
) -> Callable[P, Awaitable[R]]:
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        context: Context | None = None
        for arg in itertools.chain(args, kwargs.values()):
            if isinstance(arg, Context):
                context = arg
                break
        tg_user_id = context._user_id  # noqa: SLF001
        if tg_user_id is None:
            raise RuntimeError("No user_id in context")
        user_repo = await context.dishka_container.get(UserRepository)
        try:
            user = await user_repo.get_by_telegram_id(tg_user_id)
        except UserNotFoundError:
            user = await user_repo.create(telegram_id=tg_user_id)
        context.user = user
        return await func(*args, **kwargs)

    return wrapper
