
"""
A comprehensive test script for all MarkdownV2 formatting options.
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
    """Sends a single, comprehensive MarkdownV2 message."""

    # --- Message 1: Telegram MarkdownV2 Syntax ---
    message1 = """
*Single Asterisk Bold*
_Single Underscore Italic_
__Double Underscore Underline__
~Tilde Strikethrough~
||Spoiler Text||

*Lists*
\- Escaped Hyphen List Item 1
\- Escaped Hyphen List Item 2
\+ Escaped Plus List Item 1
\+ Escaped Plus List Item 2
\* Escaped Asterisk List Item

*Code*
`Inline Code`
```python
# Code Block
def hello():
    return "world"
```
"""

    # --- Message 2: GitHub Flavored Markdown (GFM) Syntax ---
    message2 = """
**Double Asterisk Bold**
*Single Asterisk Italic*

* Unescaped Asterisk List 1
* Unescaped Asterisk List 2

- Unescaped Hyphen List 1
- Unescaped Hyphen List 2
"""

    await update.message.reply_text("--- Sending Telegram MarkdownV2 Test Message ---")
    try:
        await update.message.reply_text(message1, parse_mode=ParseMode.MARKDOWN_V2)
        logger.info("Successfully sent the Telegram MarkdownV2 message.")
    except Exception as e:
        logger.error(f"Failed to send Telegram MarkdownV2 message: {e}")
        await update.message.reply_text(f"Failed to send Telegram MarkdownV2 message: {e}")

    await update.message.reply_text("\n--- Sending GitHub Flavored Markdown (GFM) Test Message ---")
    try:
        await update.message.reply_text(message2, parse_mode=ParseMode.MARKDOWN_V2)
        logger.info("Successfully sent the GFM message.")
    except Exception as e:
        logger.error(f"Failed to send GFM message: {e}")
        await update.message.reply_text(f"Failed to send GFM message: {e}")

def main() -> None:
    """Starts the test bot."""
    load_dotenv(override=True)
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found!")
        return

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("test", send_test_message))
    
    logger.info("Starting comprehensive Markdown test bot... Send /test to begin.")
    application.run_polling()

if __name__ == "__main__":
    main()
