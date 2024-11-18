from telegram import Message
from telegram.ext import CommandHandler

from newsmgrbot.context import Context
from newsmgrbot.utils import message


class HelpHandler(CommandHandler[Context, None]):
    def __init__(self) -> None:
        super().__init__(
            command="help",
            callback=_callback,
            filters=None,
            block=False,
            has_args=None,
        )


@message
async def _callback(message: Message, _: Context) -> None:
    await message.reply_text(
        """<b>My commands</b>

/start — introduction message.
/help — help message.
/privacy — privacy policy.

/sources — manage news sources.""",
        reply_to_message_id=message.id,
    )
