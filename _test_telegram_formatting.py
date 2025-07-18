"""
A temporary script to isolate and test the absolute basics of MarkdownV2.
"""
import os
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

async def test_formatting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a single, ultra-simple formatted message."""

    # The simplest possible valid MarkdownV2 message.
    message = "This is *bold text* and this is `inline code`\."

    await update.message.reply_text("--- Sending Simplest Possible Test Case ---")
    try:
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)
        logger.info("Successfully sent the simple test message.")
    except Exception as e:
        logger.error(f"Failed to send the simple test message: {e}")

def main() -> None:
    """Starts the simplified test bot."""
    load_dotenv(override=True)
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        return

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("test", test_formatting))
    
    logger.info("Starting simplified formatting test bot... Send /test to begin.")
    application.run_polling()
    logger.info("Test bot stopped.")

if __name__ == "__main__":
    main()