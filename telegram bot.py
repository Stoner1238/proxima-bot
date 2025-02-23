import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up API keys
TELEGRAM_BOT_TOKEN = os.getenv("AIzaSyCtIbIdFzOD30o5uLd3AMSKXnrgtWRulRQ", "your-telegram-bot-token")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Function to process user messages with Gemini AI
def ask_gemini(user_message):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_message)
        return response.text if response else "I couldn't understand that."
    except Exception as e:
        return f"Error: {str(e)}"

# Handle start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I am your AI-powered Telegram bot. Ask me anything!")

# Handle incoming messages
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    ai_response = ask_gemini(user_message)
    await update.message.reply_text(ai_response)

# Main function to run the bot
def main():
    app = Application.builder().token(7908025680:AAE9UbmSlQKSPzixHIBZa0Bs0rTvAC2R_EI).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
