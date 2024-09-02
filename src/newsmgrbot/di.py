import functools
import itertools
from collections.abc import Awaitable, Callable
from typing import Any

from dishka.integrations.base import wrap_injection

from newsmgrbot.context import Context


def inject[**P, R](func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    injected_func = wrap_injection(
        func=func,
        container_getter=lambda args, kwargs: _find_context(*args, **kwargs).dishka_container,
        is_async=True,
    )

    @functools.wraps(injected_func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        context: Context = _find_context(*args, **kwargs)
        async with context.bot_data.dishka_container() as sub_container:
            context.dishka_container = sub_container
            return await injected_func(*args, **kwargs)

    return wrapper


def _find_context(*args: Any, **kwargs: Any) -> Context:  # noqa: ANN401
    for arg in itertools.chain(args, kwargs.values()):
        if isinstance(arg, Context):
            return arg
    raise RuntimeError("Context not found")
