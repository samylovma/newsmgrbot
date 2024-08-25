from telegram import Update
from telegram.ext import ContextTypes


async def help_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """<b>My commands</b>

/start — this message.
/help — this message.

/sources — manage news sources.

/today — today news for you.""",
        reply_to_message_id=update.message.id,
    )
