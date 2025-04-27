import logging
import requests
from bs4 import BeautifulSoup
import time
import asyncio
from threading import Thread
from telegram import Bot
import nest_asyncio
import os
from flask import Flask
import telegram
from telegram.ext import Updater, CommandHandler

# Initialize Flask app
app = Flask(__name__)

# Telegram Bot configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telegram.Bot(token=TELEGRAM_TOKEN)

nest_asyncio.apply()

# Telegram Bot Configuration
TELEGRAM_TOKEN = '7743658548:AAH01KLaCFq7h9GLb_ABH5TsccTwRUVsA2Q'
CHAT_ID = '5395444623'

# === CONFIGURATION ===
URL = "https://www.usvisaappt.com/visaapplicantui/home/appointment/slot?type=POST&appUUID=257348e0-0b79-4e6b-be0f-28ad4618e6f9&applicantId=32727BDE5DCA&ofcAppointmentDate="
CHECK_INTERVAL = 300  # seconds (5 minutes)

# Define the command to get the chat ID
def get_chat_id(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text(f"Your chat ID is: {chat_id}")

# Set up the bot
def start_telegram_bot():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add the /getchatid command handler
    dp.add_handler(CommandHandler("getchatid", get_chat_id))

    # Start the bot
    updater.start_polling()
    updater.idle()

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Function to log chat ID of any incoming message
async def log_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Log the chat ID to the console
    print(f"Received a message from chat ID: {update.message.chat_id}")
    
    # Optionally, respond to the user
    await update.message.reply_text("Message received, your chat ID is logged.")

# Initialize the bot with the token
application = Application.builder().token("7743658548:AAH01KLaCFq7h9GLb_ABH5TsccTwRUVsA2Q").build()

# Add the message handler for all incoming text messages
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_chat_id))

# Run the bot (start polling for messages)
application.run_polling()


# Start Telegram bot in a separate thread
def run_telegram_bot():
    Thread(target=start_telegram_bot).start()

async def send_telegram_alert():
    message = "🚨 Appointment slot might be available! Check AVATS now: https://www.usvisaappt.com/visaapplicantui/home/appointment/slot?type=POST&appUUID=257348e0-0b79-4e6b-be0f-28ad4618e6f9&applicantId=32727BDE5DCA&ofcAppointmentDate="
    await bot.send_message(chat_id=CHAT_ID, text=message)
    print("Telegram alert sent! 🚀")

def check_avats():
    while True:
        print("Checking AVATS...")
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text().lower()
        if "no appointments" not in page_text:
            asyncio.run(send_telegram_alert())
        else:
            print("No appointment slots yet.")
        time.sleep(CHECK_INTERVAL)

# Route for home page
@app.route('/')
def home():
    return 'AVITS Monitor is running...'

# Start the Flask server and background thread
if __name__ == "__main__":
    # Start background thread for checking AVATS
    Thread(target=check_avats, daemon=True).start()

    # Start the Telegram bot in a separate thread
    run_telegram_bot()

    # Start Flask server
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Function to get chat ID
def get_chat_id(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    update.message.reply_text(f"Your chat ID is: {chat_id}")

# Enable logging to capture bot's behavior and errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to log errors
def error(update, context):
    logger.warning(f'Update {update} caused error {context.error}')
dp.add_error_handler(error)

def get_chat_id(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    print(f"Received chat ID: {chat_id}")  # Debug print
    update.message.reply_text(f"Your chat ID is: {chat_id}")

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Initialize the bot with the token and dispatcher
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Define the command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bot is working!")

# Add the handler to the application
application.add_handler(CommandHandler("start", start))

# Run the bot
application.run_polling()


# Set up the bot
def main():
    TELEGRAM_TOKEN = '7743658548:AAH01KLaCFq7h9GLb_ABH5TsccTwRUVsA2Q'  # Replace with your bot token
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher

    # Add the /getchatid command handler
    dp.add_handler(CommandHandler("getchatid", get_chat_id))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

