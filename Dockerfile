# 🔧 Base Python optimisée
FROM python:3.11.9-slim

# 📁 Répertoire de travail
WORKDIR /app

# 📦 Dépendances système pour pyautogui, opencv, etc.
RUN apt-get update && apt-get install -y \
    libx11-dev libxtst-dev libxcomposite-dev libxcursor-dev libxdamage-dev \
    libxrandr-dev libxi-dev libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender1 \
    libzbar0 libjpeg-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev \
    && rm -rf /var/lib/apt/lists/*

# 📦 Copie du code
COPY . .
# Rendre le script exécutable
RUN chmod +x start.sh


# 🐍 Installation des dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# 🌐 Port utilisé par Flask (Render injecte $PORT automatiquement)
EXPOSE 10000

# 🏁 Permet d’exécuter le script au démarrage
RUN chmod +x start.sh
CMD ["./start.sh"]
