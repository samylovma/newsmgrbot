from telegram import Update
from telegram.ext import ContextTypes


async def help_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """<b>My commands</b>

/start — introduction message.
/help — help message.
/privacy — privacy policy.

/sources — manage news sources.""",
        reply_to_message_id=update.message.id,
    )
