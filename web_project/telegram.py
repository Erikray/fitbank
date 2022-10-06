import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

def send_message(chat_id, message):
    try:
        data = {"chat_id": chat_id, "text": message}
        url = "https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_TOKEN)
        requests.post(url, data)
    except Exception as e:
        print("Erro no sendMessage:", e)