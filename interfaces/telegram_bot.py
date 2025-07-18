"""
This module implements the Telegram bot interface for the agent.

It uses the python-telegram-bot library to connect to Telegram and handle messages.
The core agent logic is reused from the agent.factory module.
"""
import os
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from telegram.error import BadRequest
from agent.factory import create_agent, get_initial_messages
from langchain_core.messages import HumanMessage
from telegramify_markdown import markdownify
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Agent Initialization ---
# We create the agent once when the bot starts up.
graph, memory = create_agent()
# --- End of Initialization ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_html(
        "👋 Hello! I am your personal assistant. Send me a message to get started."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming text messages and passes them to the agent."""
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    message_text = update.message.text

    logger.info(f"Received message from user {user_id} in chat {chat_id}: {message_text}")

    # Each user gets their own conversation history, managed by their chat_id.
    config = {"configurable": {"thread_id": str(chat_id)}}

    # Get the initial system prompt if it's a new conversation
    initial_messages = get_initial_messages(memory, config)
    if initial_messages:
        graph.update_state(config, {"messages": initial_messages})

    # Stream the agent's response
    response_message = ""
    async for event in graph.astream({"messages": [HumanMessage(content=message_text)]}, config, stream_mode="values"):
        # The final output is always the last message in the list
        final_message = event["messages"][-1]
        if final_message.content:
            response_message = final_message.content

    logger.info(f"Sending response to chat {chat_id}: {response_message}")
    
    # Convert the agent's GFM response to Telegram's MarkdownV2
    converted_message = markdownify(response_message)
    
    try:
        await update.message.reply_text(converted_message, parse_mode=ParseMode.MARKDOWN_V2)
    except BadRequest as e:
        logger.error(f"Failed to send converted message, sending as plain text. Error: {e}")
        await update.message.reply_text(response_message)



def main() -> None:
    """Starts the bot."""
    load_dotenv(override=True)
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    logger.info("Starting Telegram bot...")
    application.run_polling()
    logger.info("Telegram bot stopped.")


if __name__ == "__main__":
    main()
