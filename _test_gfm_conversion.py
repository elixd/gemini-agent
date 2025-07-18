
"""
A test script to convert a GitHub Flavored Markdown (GFM) string
to a Telegram MarkdownV2-compliant string and send it.
"""
import os
import re
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def convert_gfm_to_markdownv2(text: str) -> str:
    """
    Performs a best-effort conversion of a GFM string to MarkdownV2.
    """
    # 1. Convert GFM bold (**text**) to MarkdownV2 bold (*text*)
    text = re.sub(r'\*\*(.*?)\*\*', r'*\1*', text)

    # 2. Convert GFM lists (* item, - item) to MarkdownV2 lists (\\- item)
    text = re.sub(r'^\s*[\*\-]\s', r'\\- ', text, flags=re.MULTILINE)

    # 3. Escape all 18 reserved characters. This is crucial.
    # The characters are: _ * [ ] ( ) ~ ` > # + - = | { } . !
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    # We use a lambda to avoid re-escaping the backslashes we just added for lists
    text = re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

    return text

async def send_test_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Converts a GFM string and sends it."""

    gfm_message = """
**This is GFM bold.**

Here is a list:
* Item 1
* Item 2
- Item A
- Item B

This is a sentence with a period. And an exclamation mark!
"""

    converted_message = convert_gfm_to_markdownv2(gfm_message)

    await update.message.reply_text("--- Sending Original GFM (will fail) ---")
    try:
        await update.message.reply_text(gfm_message, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as e:
        await update.message.reply_text(f"As expected, this failed: {e}")

    await update.message.reply_text("\n--- Sending Converted MarkdownV2 ---")
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
    
    logger.info("Starting GFM conversion test bot... Send /test to begin.")
    application.run_polling()

if __name__ == "__main__":
    main()

