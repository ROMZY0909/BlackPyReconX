@echo off
REM 🚀 Script de build rapide pour payload Windows
REM Utilise packager.py pour générer le .exe furtif

echo [*] Activation de l’environnement virtuel...
call ..\env\Scripts\activate.bat

echo [*] Génération du payload Windows furtif...
python packager.py

echo [✔] Payload généré dans build\output\payload_windows.exe

pause
