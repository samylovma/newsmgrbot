from telegram import Update
from telegram.ext import ContextTypes


async def start_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! I'm @newsmgrbot. To get started choose your /sources.",
        reply_to_message_id=update.message.id,
    )
