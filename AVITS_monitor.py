import requests
from bs4 import BeautifulSoup
import time
import asyncio
from telegram import Bot
import nest_asyncio
import os

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']



nest_asyncio.apply()

# === CONFIGURATION ===
URL = "https://www.usvisaappt.com/visaapplicantui/home/appointment/slot?type=POST&appUUID=257348e0-0b79-4e6b-be0f-28ad4618e6f9&applicantId=32727BDE5DCA&ofcAppointmentDate="  # Your AVATS Accra page link
CHECK_INTERVAL = 300  # seconds (5 minutes)

# Telegram Bot Configuration
TELEGRAM_TOKEN = '7743658548:AAH01KLaCFq7h9GLb_ABH5TsccTwRUVsA2Q'
CHAT_ID = '5395444623'

async def send_telegram_alert():
    bot = Bot(token=TELEGRAM_TOKEN)
    message = "🚨 Appointment slot might be available! Check AVATS now: https://www.usvisaappt.com/visaapplicantui/home/appointment/slot?type=POST&appUUID=257348e0-0b79-4e6b-be0f-28ad4618e6f9&applicantId=32727BDE5DCA&ofcAppointmentDate="
    await bot.send_message(chat_id=CHAT_ID, text=message)
    print("Telegram alert sent! 🚀")

def check_avats():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text().lower()
    if "no appointments" not in page_text:  # Adjust based on AVATS page
        asyncio.get_event_loop().run_until_complete(send_telegram_alert())

while True:
    check_avats()
    time.sleep(CHECK_INTERVAL)
