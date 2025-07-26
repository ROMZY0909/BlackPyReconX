
🕷️ BlackPyReconX

BlackPyReconX est un framework avancé de cybersécurité offensive simulant une opération Red Team complète. Il prend en charge l'analyse OSINT, le scan réseau, l'exploitation système et web, la post-exploitation, l'exfiltration de données, la génération de rapports, et l'automatisation via bot Telegram. Le projet est compatible Windows, Android et Linux.

------------------------------------------------------------
🚀 Fonctionnalités principales

| Module             | Description |
|--------------------|-------------|
| 🔍 osint.py        | Analyse OSINT avec Shodan, AbuseIPDB, ip-api |
| 🌐 scanner.py      | Scan de ports et découverte réseau local |
| 🐞 exploit_web.py  | Détection de vulnérabilités web (XSS, SQLi, LFI...) |
| 💻 exploit_sys.py  | Reverse shell, keylogger, screenshot, webcam |
| 🧬 persistence.py  | Mécanismes de persistance (Windows/Linux/Android) |
| 📦 exfiltration.py | Exfiltration de fichiers/dossiers compressés |
| 🛡 evasion.py      | Contournement antivirus, obfuscation, encodage |
| 🔐 crypto_tools.py | Stéganographie, chiffrement Fernet |
| 📄 reporting.py    | Génération de rapports texte et PDF |
| 🤖 telegram_bot.py | Contrôle distant via bot Telegram (/scan, /rapport...) |
| 🏗 packager.py     | Générateur automatique de payloads (.exe/.sh) |

------------------------------------------------------------
🧱 Structure du projet

(main.py, .env, requirements.txt, modules/, telegram_bot/, agents/, build/, data/, outputs/)

------------------------------------------------------------
⚙️ Installation

1. Cloner le projet :
    git clone https://github.com/votre-utilisateur/BlackPyReconX.git
    cd BlackPyReconX

2. Créer un environnement virtuel :
    python -m venv .venv
    .venv\Scripts\activate   (Windows)
    source .venv/bin/activate  (Linux/macOS)

3. Installer les dépendances :
    pip install -r requirements.txt

------------------------------------------------------------
🔑 Fichier .env requis :

SHODAN_API_KEY=your_key
ABUSEIPDB_API_KEY=your_key
IPINFO_API_KEY=your_key
TELEGRAM_BOT_TOKEN=your_bot_token
BASE_WEBHOOK_URL=https://votre-app.onrender.com
TELEGRAM_SECRET_TOKEN=secret
FERNET_KEY=clé_de_chiffrement

------------------------------------------------------------
🧪 Lancement

▶️ Mode CLI local :
    python main.py

🌐 Mode Web (Flask) :
    python main.py --web

🤖 Mode Telegram :
    python telegram_bot/set_webhook.py
    Utiliser Telegram :
        /menu, /scan 8.8.8.8, /rapport

------------------------------------------------------------
⚔️ Génération de payloads

    python build/packager.py --target windows
    python build/packager.py --target android
    python build/packager.py --target unix

Fichiers générés dans build/dist/

------------------------------------------------------------
📊 Scénarios de test

- Reverse Shell Windows : exploit_sys.py
- Screenshot distant : screenshot()
- Keylogger Android : agent_android.sh via Termux
- OSINT automatique : /osint 1.1.1.1
- Exfiltration dossiers : /exfiltrate_path /sdcard/DCIM/

------------------------------------------------------------
🧠 Technologies

- Python 3.11+
- Flask
- PyInstaller
- WeasyPrint
- python-telegram-bot 20.7
- Render

------------------------------------------------------------
⚠️ Avertissement

Projet à usage **strictement légal** pour l’éducation, lab, ou test de pénétration autorisé.
L’auteur décline toute responsabilité en cas d’abus.

------------------------------------------------------------
👤 Auteur

Thomas Ouattara – Cybersecurity Engineer – Côte d’Ivoire

------------------------------------------------------------
📜 Licence

MIT – Libre usage et modification sous réserve de respect de la loi.
