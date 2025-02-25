import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, CallbackContext
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load tokens from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN is missing. Set it in Railway variables!")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing. Set it in Railway variables!")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Function to process user messages with Gemini AI
def ask_gemini(user_message):
    try:
        response = genai.generate_text(user_message)  # Adjust based on Gemini API usage
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"  # ✅ Now 'e' is properly defined

# Handle /start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I am your AI-powered Telegram bot. Ask me anything!")

# Handle messages
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    ai_response = ask_gemini(user_message)
    await update.message.reply_text(ai_response)

# Handle new members joining
async def welcome_message(update: Update, context: CallbackContext):
    for new_member in update.message.new_chat_members:
        username = new_member.username if new_member.username else new_member.full_name
        welcome_text = f"👋 Welcome, @{username}! 🎉 We're happy to have you here. Feel free to ask questions and enjoy your stay!"
        await update.message.reply_text(welcome_text)

# Main function to run the bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_message))  # Auto-welcome users

    # Start bot
    logger.info("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
