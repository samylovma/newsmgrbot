from telegram import LinkPreviewOptions, Update
from telegram.ext import ContextTypes


async def privacy_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text="https://telegram.org/privacy-tpa",
        link_preview_options=LinkPreviewOptions(is_disabled=False, prefer_large_media=True),
        reply_to_message_id=update.message.id,
    )
