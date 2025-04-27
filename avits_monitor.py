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

# Initialize Flask app
app = Flask(__name__)

# Telegram Bot configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telegram.Bot(token=TELEGRAM_TOKEN)

nest_asyncio.apply()

# === CONFIGURATION ===
URL = "https://www.usvisaappt.com/visaapplicantui/home/appointment/slot?type=POST&appUUID=257348e0-0b79-4e6b-be0f-28ad4618e6f9&applicantId=32727BDE5DCA&ofcAppointmentDate="
CHECK_INTERVAL = 300  # seconds (5 minutes)

# Telegram Bot Configuration
TELEGRAM_TOKEN = '7743658548:AAH01KLaCFq7h9GLb_ABH5TsccTwRUVsA2Q'
CHAT_ID = '5395444623'

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
    # Start background thread
    Thread(target=check_avats, daemon=True).start()

    # Start Flask server
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
