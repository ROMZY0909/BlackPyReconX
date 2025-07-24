# telegram/set_webhook.py

import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

# ✅ Chargement des variables d'environnement
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = os.getenv("BASE_WEBHOOK_URL")  # Ex: https://blackpyreconx.onrender.com
SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN")

# ✅ Vérification stricte
if not TOKEN or not BASE_URL:
    raise EnvironmentError("❌ TELEGRAM_BOT_TOKEN ou BASE_WEBHOOK_URL manquant dans .env")

if not BASE_URL.startswith("https://"):
    raise ValueError("❌ BASE_WEBHOOK_URL doit commencer par https://")

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
            print(f"✅ Webhook Telegram activé : {FULL_WEBHOOK_URL}")
            if SECRET_TOKEN:
                print("🔒 Secret token utilisé pour validation sécurisée.")
        else:
            print("❌ Impossible de définir le webhook.")

    except Exception as e:
        print(f"❌ Erreur lors de set_webhook() : {e}")

if __name__ == "__main__":
    asyncio.run(set_webhook())
