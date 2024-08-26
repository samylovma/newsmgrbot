from dishka import FromDishka
from telegram import Update
from telegram.ext import ContextTypes

from newsmgrbot.di import inject
from newsmgrbot.services.user import UserService


@inject
async def auth_callback(
    update: Update,
    _: ContextTypes.DEFAULT_TYPE,
    user_service: FromDishka[UserService],
) -> None:
    if tg_user := update.effective_user:
        await user_service.get_or_upsert(tg_id=tg_user.id)
