
"""
A comprehensive test script for the `telegramify-markdown` library.
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
    """Sends a comprehensive set of test messages."""

    # --- Message 1: Raw MarkdownV2 for baseline ---
    raw_markdownv2 = (
        "*This is a raw MarkdownV2 message*\.\n\n"
        "\- It uses escaped hyphens for lists\.\n"
        "\- It requires manual escaping of all 18 reserved characters\."
    )

    # --- Message 2: Complex GFM for conversion ---
    gfm_message = """
# This is a GFM Heading

**This is bold text.**

Here is a nested list:
* Item 1
  * Sub-item A
  * Sub-item B
* Item 2

Here is a Python code block:
```python
def hello():
    print("Hello, from GFM!")
```

And a table (which is not supported by Telegram):
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""

    converted_message = markdownify(gfm_message)

    await update.message.reply_text("--- 1. Sending Raw, Manually-Crafted MarkdownV2 ---")
    try:
        await update.message.reply_text(raw_markdownv2, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as e:
        await update.message.reply_text(f"Failed: {e}")

    await update.message.reply_text("\n--- 2. Sending GFM Converted with `telegramify-markdown` ---")
    try:
        await update.message.reply_text(converted_message, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as e:
        await update.message.reply_text(f"Failed: {e}")

def main() -> None:
    """Starts the test bot."""
    load_dotenv(override=True)
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found!")
        return

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("test", send_test_message))
    
    logger.info("Starting comprehensive telegramify test bot... Send /test to begin.")
    application.run_polling()

if __name__ == "__main__":
    main()

