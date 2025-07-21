# telegram/set_webhook.py

import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = os.getenv("BASE_WEBHOOK_URL")  # Ex: https://tonprojet.onrender.com
SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN")  # Optionnel

if not TOKEN or not BASE_URL:
    raise EnvironmentError("❌ Variables TELEGRAM_BOT_TOKEN ou BASE_WEBHOOK_URL manquantes dans .env")

WEBHOOK_PATH = "/telegram/webhook"
FULL_WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)

async def set_webhook():
    try:
        success = await bot.set_webhook(
            url=FULL_WEBHOOK_URL,
            secret_token=SECRET_TOKEN if SECRET_TOKEN else None
        )
        if success:
            print(f"✅ Webhook défini avec succès : {FULL_WEBHOOK_URL}")
        else:
            print("❌ Échec lors de la définition du webhook.")
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    asyncio.run(set_webhook())
