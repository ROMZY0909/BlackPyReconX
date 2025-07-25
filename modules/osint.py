import os
import sys
import requests
from pathlib import Path
from datetime import datetime

# ✅ Ajout dynamique du chemin racine pour import universel
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ✅ Imports internes
from modules.utils import get_api_keys, is_valid_ip

# 📂 Chemin de sortie
OUTPUT_PATH = Path(project_root) / "outputs" / "osint.txt"
api = get_api_keys()

# === 🔍 Requêtes API ===
def ipinfo_lookup(ip, token):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json?token={token}", timeout=5)
        return r.json()
    except Exception as e:
        return {"error": f"Échec ipinfo.io : {e}"}

def ipapi_lookup(ip):
    try:
        r = requests.get(f"{api['IPAPI_URL']}{ip}", timeout=5)
        return r.json()
    except Exception as e:
        return {"error": f"Échec ip-api.com : {e}"}

def abuseipdb_lookup(ip, key):
    try:
        headers = {"Accept": "application/json", "Key": key}
        params = {"ipAddress": ip}
        r = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params, timeout=5)
        return r.json().get("data", {})
    except Exception as e:
        return {"error": f"Échec abuseipdb : {e}"}

def shodan_lookup(ip, key):
    try:
        r = requests.get(f"https://api.shodan.io/shodan/host/{ip}?key={key}", timeout=5)
        return r.json()
    except Exception as e:
        return {"error": f"Échec shodan.io : {e}"}

# === 🧾 Formatage des résultats lisibles ===
def format_osint_result(ip, results):
    lines = [f"📡 Résultats OSINT pour {ip}", "─" * 40, f"🕒 Date : {datetime.now()}"]

    # IP-API
    ipapi = results.get("ip-api", {})
    lines.append("\n🌐 IP-API")
    lines.append(f"Pays      : {ipapi.get('country', 'N/A')}")
    lines.append(f"Ville     : {ipapi.get('city', 'N/A')}")
    lines.append(f"ISP       : {ipapi.get('isp', 'N/A')}")
    lines.append(f"Organisation : {ipapi.get('org', 'N/A')}")

    # IPInfo
    ipinfo = results.get("ipinfo", {})
    lines.append("\n🔍 IPInfo.io")
    lines.append(f"ASN       : {ipinfo.get('org', 'N/A')}")
    lines.append(f"Région    : {ipinfo.get('region', 'N/A')}")
    lines.append(f"Localisation : {ipinfo.get('loc', 'N/A')}")

    # AbuseIPDB
    abuse = results.get("abuseipdb", {})
    lines.append("\n🚨 AbuseIPDB")
    lines.append(f"Score de risque : {abuse.get('abuseConfidenceScore', 'N/A')} / 100")
    lines.append(f"Pays signalé   : {abuse.get('countryCode', 'N/A')}")
    lines.append(f"Domaines liés  : {abuse.get('domain', 'N/A')}")

    # Shodan
    shodan = results.get("shodan", {})
    lines.append("\n🔦 Shodan")
    ports = [str(p) for p in shodan.get("ports", [])]
    lines.append(f"Ports ouverts : {', '.join(ports) if ports else 'Aucun'}")

    return "\n".join(lines)

# 💾 Sauvegarde
def save_osint_result(ip, formatted_text):
    try:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n\n{formatted_text}\n")
        print(f"✅ Rapport OSINT sauvegardé dans {OUTPUT_PATH}")
    except Exception as e:
        print(f"❌ Erreur sauvegarde : {e}")

# 🎯 Fonction principale CLI / externe
def osint_main(ip):
    if not is_valid_ip(ip):
        print(f"❌ IP invalide : {ip}")
        return {"error": "IP invalide"}

    results = {}
    print(f"🔍 OSINT en cours pour {ip}...\n")

    # Appels API
    results["ipinfo"] = ipinfo_lookup(ip, api["IPINFO_API_KEY"]) if api.get("IPINFO_API_KEY") else {"error": "Clé manquante"}
    results["ip-api"] = ipapi_lookup(ip)
    results["abuseipdb"] = abuseipdb_lookup(ip, api["ABUSEIPDB_API_KEY"]) if api.get("ABUSEIPDB_API_KEY") else {"error": "Clé manquante"}
    results["shodan"] = shodan_lookup(ip, api["SHODAN_API_KEY"]) if api.get("SHODAN_API_KEY") else {"error": "Clé manquante"}

    formatted = format_osint_result(ip, results)
    print(formatted)
    save_osint_result(ip, formatted)
    return results  # Telegram utilisera ça

# ✅ Fonction externe utilisée par Telegram et main.py
def run(ip):
    return osint_main(ip)

# 🔁 Mode CLI
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Module OSINT BlackPyReconX")
    parser.add_argument("ip", help="Adresse IP cible")
    args = parser.parse_args()
    osint_main(args.ip)
