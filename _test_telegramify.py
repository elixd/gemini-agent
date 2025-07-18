"""
A test script to confirm the `telegramify-markdown` library works.
"""
import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from telegramify_markdown import markdownify

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def send_test_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Converts a GFM string using telegramify-markdown and sends it."""

    gfm_message = """
**This is GitHub Flavored Markdown.**

Here is a list:
* Item 1
* Item 2

And a second list:
- Item A
- Item B

This should be rendered correctly by the library.
"""

    converted_message = markdownify(gfm_message)

    await update.message.reply_text("--- Sending GFM converted with `telegramify-markdown` ---")
    try:
        await update.message.reply_text(converted_message, parse_mode=ParseMode.MARKDOWN_V2)
        logger.info("Successfully sent the converted message.")
    except Exception as e:
        logger.error(f"Failed to send converted message: {e}")
        await update.message.reply_text(f"Failed to send converted message: {e}")

def main() -> None:
    """Starts the test bot."""
    load_dotenv(override=True)
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found!")
        return

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("test", send_test_message))
    
    logger.info("Starting telegramify-markdown test bot... Send /test to begin.")
    application.run_polling()

if __name__ == "__main__":
    main()
