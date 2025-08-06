import os
import requests
import time
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

bot = Bot(token=BOT_TOKEN)

def get_latest_result():
    try:
        print("Checking site for latest result...")
        res = requests.get("https://wingo-p1-proxy.onrender.com", timeout=5).json()
        return res['data']['period'], res['data']['result']
    except Exception as e:
        print("ERROR fetching result:", e)
        return None, None

def get_color(result):
    if not result:
        return None
    return "BIG" if result[0] in ['6','7','8','9'] else "SMALL" if result[0] in ['1','2','3','4'] else "TIE"

def send_prediction(period, prediction):
    msg = f"""📢 AI WINGO 3 min Prediction
🎲 Round: {period}
🔮 Prediction: {prediction}
💸 Registration Link - CHECK ON CHANNEL BIO OR PIN MESSAGE
📊 USE 3X INVESTMENT AFTER LOSS"""
    bot.send_message(chat_id=CHANNEL_USERNAME, text=msg)
    print(f"[{period}] Predicted: {prediction}")

def send_sticker():
    sticker_id = "CAACAgUAAx0CdJ0mZgABAjZlZYbYRCkFiOYtvHw5EfIQT0qz9vUAAh8DAAIE1sFV-XceezH7Mx0zBA"
    bot.send_sticker(chat_id=CHANNEL_USERNAME, sticker=sticker_id)
    print("✅ Sent win sticker")

last_period = None
last_prediction = None
last_result = None

print("🤖 BOT STARTED")

while True:
    period, result = get_latest_result()
    print("Latest period:", period, "| Result:", result)
    if period and period != last_period:
        color = get_color(result)
        if last_prediction and last_result:
            if last_prediction == last_result:
                send_sticker()
                prediction = last_prediction
            else:
                prediction = "BIG" if last_prediction == "SMALL" else "SMALL"
        else:
            prediction = color or "BIG"
        send_prediction(period, prediction)
        last_period, last_result, last_prediction = period, color, prediction
    time.sleep(10)
