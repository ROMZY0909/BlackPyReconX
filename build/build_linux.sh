#!/bin/bash
# 🚀 Script de build rapide pour payload Linux

echo "[*] Activation de l’environnement virtuel..."
source ../env/bin/activate

echo "[*] Compilation du payload Linux..."
pyinstaller --noconfirm --onefile --clean --distpath output ../agents/linux/agent_linux.py

echo "[✔] Payload Linux généré dans build/output/"
