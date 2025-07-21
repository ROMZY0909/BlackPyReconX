# modules/utils.py

import os
import socket
import hashlib
from datetime import datetime
from ipaddress import ip_address
from dotenv import load_dotenv

# 🔄 Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# 🔑 Centralisation des clés API et des secrets
def get_api_keys():
    return {
        # OSINT
        "SHODAN_API_KEY": os.getenv("SHODAN_API_KEY"),
        "ABUSEIPDB_API_KEY": os.getenv("ABUSEIPDB_API_KEY"),
        "IPINFO_API_KEY": os.getenv("IPINFO_API_KEY"),
        "IPAPI_URL": os.getenv("IPAPI_URL", "http://ip-api.com/json/"),

        # Telegram
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "TELEGRAM_SECRET_TOKEN": os.getenv("TELEGRAM_SECRET_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
        "BASE_WEBHOOK_URL": os.getenv("BASE_WEBHOOK_URL"),

        # Email
        "EMAIL_SENDER": os.getenv("EMAIL_SENDER"),
        "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD"),
        "SMTP_SERVER": os.getenv("SMTP_SERVER"),
        "SMTP_PORT": int(os.getenv("SMTP_PORT", 587)),
        "EMAIL_RECEIVER": os.getenv("EMAIL_RECEIVER"),

        # Chiffrement
        "FERNET_KEY": os.getenv("FERNET_KEY"),

        # Reverse Shell / Exploitation
        "ATTACKER_IP": os.getenv("ATTACKER_IP"),
        "ATTACKER_PORT": int(os.getenv("ATTACKER_PORT", 4444)),

        # Optionnel : pour génération de résumé de rapport
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")
    }

# 📁 Crée un dossier s’il n’existe pas
def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

# 📄 Écrit du texte dans un fichier
def write_to_file(filepath: str, content: str, mode="a"):
    with open(filepath, mode, encoding="utf-8") as f:
        f.write(content + "\n")

# 📄 Lit un fichier ligne par ligne
def read_lines(filepath: str):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# 🕒 Timestamp actuel formaté
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 🌐 Vérifie si une IP est bien formée
def is_valid_ip(ip: str) -> bool:
    try:
        ip_address(ip)
        return True
    except ValueError:
        return False

# 🌍 Résolution DNS d’un nom de domaine
def resolve_domain(domain: str):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

# 🔐 Génère le hash SHA-256 d’une chaîne
def hash_sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

# 📁 Génère un nom de fichier avec préfixe et horodatage
def generate_output_filename(prefix="output", extension=".txt"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}{extension}"
