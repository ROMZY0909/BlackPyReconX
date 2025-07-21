import socket
import subprocess
import platform
import threading
from datetime import datetime
from pathlib import Path

from modules.utils import is_valid_ip

# 📂 Chemin du fichier de résultats
SCAN_RESULT = Path(__file__).resolve().parent.parent / "outputs" / "scan_results.txt"

# 🌐 Services courants
COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL",
    3389: "RDP", 8080: "HTTP-Alt"
}

def ping_target(ip, count=4):
    """Effectue un ping vers la cible pour évaluer la latence"""
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
    """Estime le système d'exploitation selon le TTL"""
    if ttl >= 128:
        return "Windows"
    elif 64 <= ttl < 128:
        return "Linux/Unix"
    elif ttl < 64:
        return "Android/IoT"
    else:
        return "Inconnu"

def reverse_dns(ip):
    """Résolution DNS inverse de l'adresse IP"""
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Non résolu"

def banner_grab(ip, port):
    """Essaye de récupérer une bannière de service"""
    try:
        with socket.socket() as s:
            s.settimeout(2)
            s.connect((ip, port))
            return s.recv(1024).decode(errors="ignore").strip()
    except:
        return ""

def scan_port(ip, port, open_ports):
    """Scan un port et ajoute à la liste si ouvert"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip, port))
            service = COMMON_PORTS.get(port, "Inconnu")
            banner = banner_grab(ip, port)
            open_ports.append((port, service, banner))
    except Exception as e:
        pass  # silencieux volontairement pour performance

def ascii_ports(open_ports):
    """Affiche une barre ASCII selon la plage des ports"""
    bar = ""
    for port, _, _ in open_ports:
        if port < 1024:
            bar += "|#"
        elif port < 49152:
            bar += "|*"
        else:
            bar += "|."
    return bar

def save_results(ip, ttl, os_guess, reverse, success_rate, open_ports):
    """Sauvegarde les résultats du scan dans un fichier"""
    try:
        with open(SCAN_RESULT, "a", encoding="utf-8") as f:
            f.write(f"\n\n===== 🔍 SCAN : {ip} =====\n")
            f.write(f"🕒 Date : {datetime.now()}\n")
            f.write(f"🌐 Reverse DNS : {reverse}\n")
            f.write(f"📶 Ping Réussi : {success_rate}%\n")
            f.write(f"🧠 TTL : {ttl} → OS probable : {os_guess}\n")
            f.write("\n--- Ports ouverts ---\n")
            for port, service, banner in open_ports:
                f.write(f"🔓 {port} ({service}) | {banner}\n")
            f.write("\n--- ASCII Graph ---\n")
            f.write(ascii_ports(open_ports) + "\n")
        print(f"✅ Résultat sauvegardé dans {SCAN_RESULT}")
    except Exception as e:
        print(f"❌ Erreur sauvegarde : {e}")

def scan_main(ip, port_range=(1, 1024)):
    """Fonction principale de scan réseau"""
    if not is_valid_ip(ip):
        print(f"❌ IP invalide : {ip}")
        return []

    if port_range[0] < 1 or port_range[1] > 65535:
        print("❌ Plage de ports invalide")
        return []

    print(f"🔎 Scan TCP/UDP de {ip}...\n")
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
    save_results(ip, ttl, os_guess, reverse, ping_pct, open_ports)
    return open_ports

# 🔁 Test CLI local
if __name__ == "__main__":
    ip = input("Entrez l'IP à scanner : ").strip()
    scan_main(ip)
