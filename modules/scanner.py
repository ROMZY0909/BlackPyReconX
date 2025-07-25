import os
import sys
import socket
import subprocess
import platform
import threading
from datetime import datetime
from pathlib import Path

# ✅ Import dynamique universel
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from modules.utils import is_valid_ip

# 📂 Chemin du fichier de résultats
OUTPUT_PATH = Path(project_root) / "outputs"
SCAN_RESULT = OUTPUT_PATH / "scan_results.txt"

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL",
    3389: "RDP", 8080: "HTTP-Alt"
}

def ping_target(ip, count=4):
    system = platform.system().lower()
    param = "-n" if "windows" in system else "-c"
    cmd = ["ping", param, str(count), ip]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode()
        success = output.lower().count("ttl")
        return round((success / count) * 100)
    except Exception:
        return 0

def detect_os(ttl):
    if ttl >= 128:
        return "Windows"
    elif 64 <= ttl < 128:
        return "Linux/Unix"
    elif ttl < 64:
        return "Android/IoT"
    return "Inconnu"

def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Non résolu"

def banner_grab(ip, port):
    try:
        with socket.socket() as s:
            s.settimeout(2)
            s.connect((ip, port))
            return s.recv(1024).decode(errors="ignore").strip()
    except:
        return ""

def scan_port(ip, port, open_ports):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip, port))
            service = COMMON_PORTS.get(port, "Inconnu")
            banner = banner_grab(ip, port)
            open_ports.append((port, service, banner))
    except:
        pass

def ascii_ports(open_ports):
    bar = ""
    for port, _, _ in open_ports:
        if port < 1024:
            bar += "|#"
        elif port < 49152:
            bar += "|*"
        else:
            bar += "|."
    return bar

def format_scan_result(ip, ttl, os_guess, reverse, success_rate, open_ports):
    lines = [
        f"📡 Résultats du scan pour {ip}",
        "─" * 40,
        f"🕒 Date : {datetime.now()}",
        f"📶 Ping : {success_rate}%",
        f"🧠 TTL  : {ttl} → OS estimé : {os_guess}",
        f"🌐 Reverse DNS : {reverse}",
        "\n🔓 Ports ouverts :"
    ]
    if open_ports:
        for port, service, banner in open_ports:
            lines.append(f"- {port} ({service}) : {banner}")
    else:
        lines.append("Aucun port ouvert détecté.")

    lines.append("\n📊 ASCII Graph :")
    lines.append(ascii_ports(open_ports))

    return "\n".join(lines)

def save_results(ip, formatted):
    try:
        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
        with open(SCAN_RESULT, "a", encoding="utf-8") as f:
            f.write(f"\n\n{formatted}\n")
        print(f"✅ Résultat sauvegardé dans {SCAN_RESULT}")
    except Exception as e:
        print(f"❌ Erreur sauvegarde : {e}")

def scan_main(ip, port_range=(1, 1024)):
    if not is_valid_ip(ip):
        print(f"❌ IP invalide : {ip}")
        return None

    if port_range[0] < 1 or port_range[1] > 65535:
        print("❌ Plage de ports invalide")
        return None

    print(f"🔎 Scan en cours pour {ip}...\n")
    open_ports = []

    ping_pct = ping_target(ip)
    ttl = 128 if ping_pct > 0 else 0
    os_guess = detect_os(ttl)
    reverse = reverse_dns(ip)

    threads = []
    for port in range(port_range[0], port_range[1] + 1):
        t = threading.Thread(target=scan_port, args=(ip, port, open_ports))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    open_ports.sort()
    formatted = format_scan_result(ip, ttl, os_guess, reverse, ping_pct, open_ports)
    print(formatted)
    save_results(ip, formatted)
    return formatted  # utile pour bot Telegram

# ✅ Appel externe depuis Telegram ou main.py
def run(ip):
    return scan_main(ip)

# 🔁 Mode CLI local
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Module de scan réseau BlackPyReconX")
    parser.add_argument("ip", help="Adresse IP cible")
    parser.add_argument("--start", type=int, default=1, help="Port de début")
    parser.add_argument("--end", type=int, default=1024, help="Port de fin")
    args = parser.parse_args()
    scan_main(args.ip, port_range=(args.start, args.end))
