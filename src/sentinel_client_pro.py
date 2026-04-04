import subprocess
import requests
import json
import time
import platform

# --- CONFIGURATION (À REMPLIR) ---
SENTINEL_URL = "https://dorknetgm-sentinel.onrender.com/api/audit"
TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""
# --------------------------------

def send_telegram_alert(message):
    """Envoie une alerte prioritaire sur Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": f"🚨 [DorkNet-Alert]\n{message}", "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[!] Échec d'envoi Telegram : {e}")

def get_system_metrics():
    """Collecte les données forensics de base (Kali/Termux/Server)"""
    metrics = {
        "origin": f"System-{platform.node()}-{platform.system()}",
        "type": "Quantum-Forensics-Audit",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "network": {},
        "security": {}
    }
    try:
        # Analyse des ports (Netstat)
        netstat = subprocess.check_output("netstat -tuln | grep LISTEN", shell=True).decode()
        metrics["network"]["open_ports"] = netstat.split('\n')[:-1]

        # Analyse des utilisateurs (Forensics)
        who = subprocess.check_output("who", shell=True).decode()
        metrics["security"]["active_users"] = who.split('\n')[:-1]

        # Top 5 processus (Détection Anomalie CPU/RAM)
        top = subprocess.check_output("ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 6", shell=True).decode()
        metrics["security"]["top_processes"] = top.split('\n')[1:]
    except Exception as e:
        metrics["error"] = str(e)
    return metrics

def run_sentinel_cycle():
    data = get_system_metrics()
    print(f"[*] Audit en cours ({data['timestamp']})... Envoi à Render...")
    
    try:
        response = requests.post(SENTINEL_URL, json=data, timeout=20)
        if response.status_code == 200:
            analysis = response.json().get("analysis", "")
            print(f"[+] Analyse reçue : \n{analysis}")

            # ALGORITHME DE DÉCISION : Alerte si l'IA détecte un risque
            # On cherche des mots clés comme 'Risqué', 'Danger', 'Vulnerable' ou 'Alert'
            if any(word in analysis.upper() for word in ["RISQUÉ", "DANGER", "VULNERABLE", "ALERT", "FRAUDE"]):
                alert_msg = f"*Audit System :* {data['origin']}\n*Verdict :* RISQUE DÉTECTÉ\n\n*Détails :*\n{analysis[:500]}..."
                send_telegram_alert(alert_msg)
        else:
            print(f"[!] Erreur API Render : {response.status_code}")
    except Exception as e:
        print(f"[!] Erreur de liaison avec Sentinel : {e}")

if __name__ == "__main__":
    print("--- DorkNetGM Sentinel Client (Version Fusionnée) ---")
    while True:
        run_sentinel_cycle()
        # Audit toutes les 30 minutes pour une surveillance accrue
        print("\n[*] Veille de 30 min avant le prochain scan...")
        time.sleep(1800)
