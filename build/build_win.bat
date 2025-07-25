@echo off
:: █▀█ █░█ █░█ █ █▄░█ █▀▄ █ █░█ █░█
:: █▀▄ █▄█ ▀▄▀ █ █░▀█ █▄▀ █ ▀▄▀ █▀█

:: ✅ Configuration
set MODULE=exploit_sys.py
set OUTPUT_NAME=exploit_sys_win.exe

:: ✅ Répertoire racine
set PROJECT_ROOT=%~dp0\..
cd /d %PROJECT_ROOT%

:: ✅ Dossiers de sortie
set DIST_DIR=outputs\builds\windows
mkdir %DIST_DIR% 2>nul

:: ✅ Nettoyage précédent (optionnel)
rd /s /q build\temp 2>nul
rd /s /q build\specs 2>nul

:: ✅ Compilation avec PyInstaller
pyinstaller ^
 --onefile ^
 --noconfirm ^
 --name %OUTPUT_NAME% ^
 --distpath %DIST_DIR% ^
 --workpath build\temp ^
 --specpath build\specs ^
 modules\%MODULE%

:: ✅ Vérification
if exist %DIST_DIR%\%OUTPUT_NAME% (
    echo ✅ Compilation reussie : %DIST_DIR%\%OUTPUT_NAME%
) else (
    echo ❌ Erreur pendant la compilation
    exit /b 1
)
