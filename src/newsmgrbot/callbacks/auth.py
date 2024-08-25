from dishka import FromDishka
from telegram import Update
from telegram.ext import ContextTypes

from newsmgrbot.di import inject
from newsmgrbot.models import User
from newsmgrbot.services.user_repo import UserRepository


@inject
async def auth_callback(
    update: Update,
    _: ContextTypes.DEFAULT_TYPE,
    user_repo: FromDishka[UserRepository],
) -> None:
    if tg_user := update.effective_user:
        await user_repo.upsert(User(id=tg_user.id))
