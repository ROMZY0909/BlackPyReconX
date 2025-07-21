import base64
import codecs
import os
from cryptography.fernet import Fernet
from PIL import Image, PngImagePlugin
from io import BytesIO
from pathlib import Path

# -------------------------------------
# Chiffrement Base64
# -------------------------------------
def encrypt_base64(data: bytes) -> str:
    """Chiffrement base64"""
    return base64.b64encode(data).decode()

def decrypt_base64(data: str) -> bytes:
    """Déchiffrement base64"""
    return base64.b64decode(data.encode())

# -------------------------------------
# Chiffrement ROT13
# -------------------------------------
def encrypt_rot13(text: str) -> str:
    return codecs.encode(text, 'rot_13')

def decrypt_rot13(text: str) -> str:
    return codecs.decode(text, 'rot_13')

# -------------------------------------
# Chiffrement XOR (faible, démonstratif)
# -------------------------------------
def xor_encrypt(data: str, key: int = 42) -> str:
    return ''.join(chr(ord(c) ^ key) for c in data)

def xor_decrypt(data: str, key: int = 42) -> str:
    return xor_encrypt(data, key)

# -------------------------------------
# Chiffrement Fernet (sécurisé)
# -------------------------------------
def generate_fernet_key() -> bytes:
    return Fernet.generate_key()

def encrypt_fernet(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_fernet(token: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(token)

# -------------------------------------
# Stéganographie dans PNG
# -------------------------------------
def hide_data_in_image(image_path: str, data_to_hide: str, output_path: str = "image_stego_hidden.png"):
    """Cache une chaîne dans un PNG via les métadonnées (base64)"""
    try:
        path = Path(image_path)
        if not path.exists():
            return f"❌ Image introuvable : {image_path}"

        img = Image.open(image_path)
        metadata = PngImagePlugin.PngInfo()
        encoded = base64.b64encode(data_to_hide.encode()).decode()
        metadata.add_text("hidden", encoded)

        img.save(output_path, "PNG", pnginfo=metadata)
        return f"✅ Données cachées dans : {output_path}"
    except Exception as e:
        return f"❌ Erreur stéganographie : {e}"

def extract_data_from_image(image_path: str):
    """Extrait les données cachées via `hide_data_in_image`"""
    try:
        path = Path(image_path)
        if not path.exists():
            return f"❌ Fichier introuvable : {image_path}"

        img = Image.open(image_path)
        data = img.info.get("hidden")
        if data:
            return base64.b64decode(data.encode()).decode()
        return "❌ Aucun contenu caché trouvé dans l’image."
    except Exception as e:
        return f"❌ Erreur extraction : {e}"

# -------------------------------------
# Démo locale (à désactiver en prod)
# -------------------------------------
if __name__ == "__main__":
    secret = "import os\nprint('Code caché')"
    print(hide_data_in_image("image_stego.png", secret))
    print(extract_data_from_image("image_stego_hidden.png"))
