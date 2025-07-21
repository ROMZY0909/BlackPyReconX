import requests
import json
from pathlib import Path
from datetime import datetime

from modules.utils import get_api_keys, is_valid_ip

# 📂 Chemin de sortie pour les résultats OSINT
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "outputs" / "osint.txt"

# 🔐 Chargement des clés API via .env
api = get_api_keys()

# === 🔍 Fonctions de lookup API ===

def ipinfo_lookup(ip, token):
    """Recherche d'information via ipinfo.io"""
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json?token={token}", timeout=5)
        return r.json()
    except Exception as e:
        return {"error": f"Échec ipinfo.io : {e}"}

def ipapi_lookup(ip):
    """Recherche via ip-api.com (URL dans .env)"""
    try:
        r = requests.get(f"{api['IPAPI_URL']}{ip}", timeout=5)
        return r.json()
    except Exception as e:
        return {"error": f"Échec ip-api.com : {e}"}

def abuseipdb_lookup(ip, key):
    """Recherche de réputation via abuseipdb.com"""
    try:
        headers = {"Accept": "application/json", "Key": key}
        params = {"ipAddress": ip}
        r = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params, timeout=5)
        return r.json().get("data", {})
    except Exception as e:
        return {"error": f"Échec abuseipdb : {e}"}

def shodan_lookup(ip, key):
    """Recherche d'infos Shodan sur l'IP"""
    try:
        r = requests.get(f"https://api.shodan.io/shodan/host/{ip}?key={key}", timeout=5)
        return r.json()
    except Exception as e:
        return {"error": f"Échec shodan.io : {e}"}

# 💾 Sauvegarde des résultats OSINT
def save_osint_result(ip, results):
    """Enregistre les résultats OSINT dans outputs/osint.txt"""
    try:
        with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n\n===== 🔍 OSINT : {ip} =====\n")
            f.write(f"🕒 Date : {datetime.now()}\n")
            for source, data in results.items():
                f.write(f"\n--- {source.upper()} ---\n")
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
        print(f"✅ Résultat OSINT sauvegardé dans {OUTPUT_PATH}")
    except Exception as e:
        print(f"❌ Erreur sauvegarde : {e}")

# 🎯 Fonction principale OSINT
def osint_main(ip):
    """Lance les recherches OSINT sur l'IP"""
    if not is_valid_ip(ip):
        print(f"❌ IP invalide : {ip}")
        return

    results = {}
    print(f"🔍 OSINT en cours pour {ip}...\n")

    # ipinfo.io
    if api.get("IPINFO_API_KEY"):
        results["ipinfo"] = ipinfo_lookup(ip, api["IPINFO_API_KEY"])
    else:
        results["ipinfo"] = {"error": "Clé manquante"}

    # ip-api.com
    results["ip-api"] = ipapi_lookup(ip)

    # abuseipdb.com
    if api.get("ABUSEIPDB_API_KEY"):
        results["abuseipdb"] = abuseipdb_lookup(ip, api["ABUSEIPDB_API_KEY"])
    else:
        results["abuseipdb"] = {"error": "Clé manquante"}

    # shodan.io
    if api.get("SHODAN_API_KEY"):
        results["shodan"] = shodan_lookup(ip, api["SHODAN_API_KEY"])
    else:
        results["shodan"] = {"error": "Clé manquante"}

    # Enregistrement
    save_osint_result(ip, results)
    return results

# 🔁 Exemple d’utilisation CLI
if __name__ == "__main__":
    target = input("Entrez l'IP cible : ").strip()
    osint_main(target)
