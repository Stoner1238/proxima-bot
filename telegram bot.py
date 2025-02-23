import google.generativeai as genai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# 🔹 Set up Gemini API Key
API_KEY = "AIzaSyCtIbIdFzOD30o5uLd3AMSKXnrgtWRulRQ"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# 🔹 Initialize the Model
model = genai.GenerativeModel("gemini-pro")  

def ask_gemini(user_message):
    """ Generate AI response for a given message. """
    response = model.generate_content(user_message)  # Pass only user_message
    return response.text  # Return AI-generated text

def handle_message(update: Update, context: CallbackContext):
    """ Handle incoming user messages. """
    user_message = update.message.text  # Get user message
    ai_response = ask_gemini(user_message)  # Pass only user_message
    update.message.reply_text(ai_response)  # Reply with AI response

# 🔹 Setup Telegram Bot
TELEGRAM_BOT_TOKEN = "7908025680:AAE9UbmSlQKSPzixHIBZa0Bs0rTvAC2R_EI"  # Replace with actual bot token
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Start the bot
updater.start_polling()
updater.idle()
