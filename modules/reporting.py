import datetime
from pathlib import Path

# 📂 Répertoire des résultats
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
REPORT_PATH = OUTPUT_DIR / "rapport_final.txt"

# ✅ Créer outputs/ si absent
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def lire_fichier(path: Path) -> str:
    """Lit un fichier texte et retourne son contenu"""
    if path.exists():
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return "[Aucune donnée]"

def generate_report():
    """Génère le rapport final BlackPyReconX"""
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    sections = {
        "🕓 Début du rapport": timestamp,
        "📡 Résultats OSINT": lire_fichier(OUTPUT_DIR / "osint.txt"),
        "🧠 Résultats SCAN Réseau": lire_fichier(OUTPUT_DIR / "scan_results.txt"),
        "🌐 Vulnérabilités Web": lire_fichier(OUTPUT_DIR / "web_vulns.txt"),
        "🖥️ Exploits Système": lire_fichier(OUTPUT_DIR / "system_exploits.txt"),
        "📦 Chemin ZIP Exfiltration": str(OUTPUT_DIR / "exfiltrated.zip"),
        "📂 Contenu Dossier Exfiltré": lire_fichier(OUTPUT_DIR / "exfiltrate_path.txt"),
        "✅ Statut Opération": "Opération simulée terminée avec succès"
    }

    try:
        with open(REPORT_PATH, "w", encoding="utf-8") as rapport:
            rapport.write("======= 🕷️ Rapport Final - BlackPyReconX 🕷️ =======\n")
            for titre, contenu in sections.items():
                rapport.write(f"\n### {titre} ###\n")
                rapport.write(f"{contenu}\n")
                rapport.write("-" * 60 + "\n")
            rapport.write("\n📌 Rapport généré automatiquement par BlackPyReconX.\n")
        print(f"✅ Rapport généré avec succès : {REPORT_PATH}")
        return str(REPORT_PATH)
    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport : {e}")
        return None

# Lancement manuel
if __name__ == "__main__":
    generate_report()
