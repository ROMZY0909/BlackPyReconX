# ✅ Image de base complète pour éviter les erreurs de dpkg
FROM python:3.11.9

# 📁 Répertoire de travail
WORKDIR /app

# 📦 Copie des fichiers dans le conteneur
COPY . .

# 🛠️ Installation des dépendances système nécessaires (screenshot, keylogger, etc.)
RUN apt-get update && apt-get install -y \
    libx11-dev libxtst-dev libxcomposite-dev libxcursor-dev \
    libxdamage-dev libxrandr-dev libxi-dev libgl1-mesa-glx \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 📦 Installation des dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# 🚀 Commande de lancement
CMD ["python", "main.py"]
