#!/bin/bash

# ░█▀▀░█▀█░█░█░█▀█░█▀█░█░█░█▀▄░█░█░█░█
# ░█░░░█░█░█▀▄░█░█░█░█░░█░█░█░░░░█░░█░█
# ░▀▀▀░▀▀▀░▀░▀░▀░▀░▀▀▀░░▀░▀░▀▀▀░░▀░░░▀░

# ✅ Nom du module à packager
MODULE="exploit_sys.py"

# ✅ Nom du binaire de sortie
OUTPUT_NAME="exploit_sys_linux"

# ✅ Répertoire du projet
PROJECT_ROOT=$(dirname "$(dirname "$(realpath "$0")")")

# ✅ Dossier de sortie
DIST_DIR="$PROJECT_ROOT/outputs/builds/linux"
mkdir -p "$DIST_DIR"

echo "📦 Compilation du module $MODULE..."

# ✅ Nettoyage ancien build (optionnel)
rm -rf "$PROJECT_ROOT/build/__pycache__"
rm -rf "$PROJECT_ROOT/$OUTPUT_NAME" 2>/dev/null

# ✅ Compilation avec PyInstaller
pyinstaller \
    --onefile \
    --name "$OUTPUT_NAME" \
    --distpath "$DIST_DIR" \
    --workpath "$PROJECT_ROOT/build/temp" \
    --specpath "$PROJECT_ROOT/build/specs" \
    "$PROJECT_ROOT/modules/$MODULE"

# ✅ Vérification du binaire
if [[ -f "$DIST_DIR/$OUTPUT_NAME" ]]; then
    echo "✅ Binaire compilé avec succès : $DIST_DIR/$OUTPUT_NAME"
else
    echo "❌ Échec de la compilation"
    exit 1
fi
