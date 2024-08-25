import functools
import itertools
from collections.abc import Awaitable, Callable
from contextlib import suppress
from typing import Any, cast

from dishka import AsyncContainer
from dishka.integrations.base import wrap_injection
from telegram.ext import CallbackContext


def inject[T, **P](func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
    injected_func = wrap_injection(
        func=func,
        container_getter=_container_getter,
        is_async=True,
    )

    @functools.wraps(injected_func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        context: CallbackContext[Any, Any, Any, Any]
        for arg in itertools.chain(args, kwargs.values()):
            if isinstance(arg, CallbackContext):
                context = arg
                break
        container: AsyncContainer = context.bot_data["container"]
        async with container() as sub_container:
            setattr(context, "__dishka_sub_container", sub_container)
            result = await injected_func(*args, **kwargs)
            with suppress(AttributeError):
                delattr(context, "__dishka_sub_container")
        return result

    return wrapper


def _container_getter(args: tuple[Any, ...], kwargs: dict[str, Any]) -> AsyncContainer:
    for arg in itertools.chain(args, kwargs.values()):
        if isinstance(arg, CallbackContext):
            return cast(AsyncContainer, getattr(arg, "__dishka_sub_container"))
    raise RuntimeError("context not found")
