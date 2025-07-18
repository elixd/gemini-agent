"""
A final, correct script to demonstrate a complex MarkdownV2 message with lists.
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

async def send_test_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a single, correctly formatted complex MarkdownV2 message."""

    # This is the user's desired message, corrected for valid MarkdownV2 syntax:
    # - Lists are created by escaping the hyphen `\-`.
    # - Literal characters like `.` and `:` are escaped.
    # - Bold uses a single asterisk `*`.
    message = (
        "I can help with various software engineering tasks\\. I can:\n\n"
        "\\- *Read and write files*\\: `read_file`, `write_file`, `read_many_files`\n"
        "\\- *Navigate the file system*\\: `list_directory`, `glob`\n"
        "\\- *Search file content*\\: `search_file_content`\n"
        "\\- *Run shell commands*\\: `run_shell_command`\n"
        "\\- *Perform text replacements within files*\\: `replace`\n"
        "\\- *Search the web*\\: `google_web_search`\n"
        "\\- *Remember facts*\\: `save_memory`"
    )

    await update.message.reply_text("--- Sending Final Corrected MarkdownV2 Message ---")
    try:
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN_V2)
        logger.info("Successfully sent the message.")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        await update.message.reply_text(f"Failed to send message: {e}")

def main() -> None:
    """Starts the test bot."""
    load_dotenv(override=True)
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found!")
        return

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("test", send_test_message))
    
    logger.info("Starting final Markdown test bot... Send /test to begin.")
    application.run_polling()

if __name__ == "__main__":
    main()