[app]
title = SystemUpdate
package.name = systemupdate
package.domain = org.android.sys
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
icon.filename = icon.png
fullscreen = 0
orientation = portrait
log_level = 1

# Entrée principale
entrypoint = main.py

# Permissions Android requises
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE

# Masquer les logs + comportement furtif
android.minapi = 21
android.hidden_api_policy = unrestricted

# Cibler les architectures Android standards
android.archs = armeabi-v7a,arm64-v8a

# Mode debug pour tests
buildozer.android.debug = True

[buildozer]
log_level = 2
warn_on_root = 1

[app.android]
# Empêche les plantages liés à kivy launcher
presplash.filename = icon.png
