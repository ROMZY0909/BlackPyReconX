# main.py

import argparse
import os
import sys

# ✅ Import modules disponibles
from modules.osint import osint_main
from modules.scanner import scan_main
from modules.exfiltration import exfiltrate_all, exfiltrate_path
from modules.exploit_sys import (
    start_keylogger, take_screenshot, capture_webcam,
    exploit_system
)
from modules.reporting import generate_report
from modules.utils import banner

def run_cli():
    parser = argparse.ArgumentParser(description="🕷️ BlackPyReconX - Red Team CLI")

    parser.add_argument("--target", help="Cible IP ou domaine")
    parser.add_argument("--osint", action="store_true", help="Effectuer un OSINT")
    parser.add_argument("--scan", action="store_true", help="Scan réseau")
    parser.add_argument("--exploit_sys", action="store_true", help="Exploitation système")
    parser.add_argument("--keylogger", action="store_true", help="Lancer le keylogger")
    parser.add_argument("--screenshot", action="store_true", help="Capture d'écran")
    parser.add_argument("--webcam", action="store_true", help="Capture webcam")
    parser.add_argument("--exfil", action="store_true", help="Exfiltration générale")
    parser.add_argument("--exfiltrate_path", help="Exfiltration d'un chemin spécifique")
    parser.add_argument("--report", action="store_true", help="Génération de rapport final")

    args = parser.parse_args()

    if args.osint:
        if args.target:
            osint_main(args.target)
        else:
            print("❌ Veuillez fournir une cible avec --target")
            return

    elif args.scan:
        if args.target:
            scan_main(args.target)
        else:
            print("❌ Veuillez fournir une cible avec --target")
            return

    elif args.exploit_sys:
        if args.target:
            exploit_system(args.target)
        else:
            print("❌ Veuillez fournir une IP cible avec --target")
            return

    elif args.keylogger:
        start_keylogger()

    elif args.screenshot:
        take_screenshot()

    elif args.webcam:
        capture_webcam()

    elif args.exfil:
        exfiltrate_all()

    elif args.exfiltrate_path:
        exfiltrate_path(args.exfiltrate_path)

    elif args.report:
        generate_report()

    else:
        banner()
        parser.print_help()

if __name__ == "__main__":
    run_cli()
