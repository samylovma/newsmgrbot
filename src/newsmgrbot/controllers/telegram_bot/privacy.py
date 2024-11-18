from telegram import LinkPreviewOptions, Message
from telegram.ext import CommandHandler

from newsmgrbot.context import Context
from newsmgrbot.utils import message


class PrivacyHandler(CommandHandler[Context, None]):
    def __init__(self) -> None:
        super().__init__(
            command="privacy",
            callback=_callback,
            filters=None,
            block=False,
            has_args=None,
        )


@message
async def _callback(message: Message, _: Context) -> None:
    await message.reply_text(
        text="https://telegram.org/privacy-tpa",
        link_preview_options=LinkPreviewOptions(
            is_disabled=False, prefer_large_media=True
        ),
        reply_to_message_id=message.id,
    )
