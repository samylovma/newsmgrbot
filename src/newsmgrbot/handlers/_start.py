from telegram import Message
from telegram.ext import CommandHandler

from newsmgrbot.context import Context
from newsmgrbot.utils import message


class StartHandler(CommandHandler[Context]):
    def __init__(self) -> None:
        super().__init__(
            command="start",
            callback=_callback,
            filters=None,
            block=False,
            has_args=None,
        )


@message
async def _callback(message: Message, _: Context) -> None:
    await message.reply_text(
        "Hi! I'm @newsmgrbot. To get started choose your /sources.",
        reply_to_message_id=message.id,
    )
