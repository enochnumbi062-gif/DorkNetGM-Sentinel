import os
import json
import requests
import google.generativeai as genai
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- CONFIGURATION EXPERT (ROOT) ---
# Correction de l'erreur 404 : Utilisation du canal stable
GEN_KEY = "AIzaSyAJGP_etVbcz7bcBISYV7gD_kmPqaIv2O4"
genai.configure(api_key=GEN_KEY)

# Initialisation sans préfixe 'v1beta' pour garantir la compatibilité
model = genai.GenerativeModel('gemini-1.5-flash')

# Identifiants Telegram récupérés de vos captures
TELEGRAM_TOKEN = "8462494984:AAGs7FHpV7QWsxatcKuVgaTaB9vwLHjyYww"
TELEGRAM_CHAT_ID = "768138087"

def send_critical_alert(msg):
    """Envoie l'alerte au bot Dorknet-Sentinel"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": f"🚨 *[SENTINEL-ALERT]*\n\n{msg}",
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

# --- ROUTES API ---

@app.route('/')
def home():
    return "DorkNetGM Quantum Sentinel Hub - Systèmes & Paiements Actifs", 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "online", "engine": "Gemini-1.5-Flash"}), 200

@app.route('/api/audit', methods=['POST'])
def run_audit():
    """Route pour Kali Linux et DorkNetGM"""
    data = request.get_json()
    origin = data.get("origin", "Unknown System")
    
    prompt = f"Analyse Forensic pour {origin}. Verdict : Sûr ou Risqué ?\nDonnées: {json.dumps(data)}"
    
    try:
        # L'appel qui ne causera plus d'erreur 404
        response = model.generate_content(prompt)
        verdict = response.text
        
        # Alerte automatique Telegram si danger détecté
        if any(word in verdict.upper() for word in ["RISQUÉ", "DANGER", "FRAUDE"]):
            send_critical_alert(f"Menace sur {origin} !\n\n{verdict[:300]}")

        return jsonify({"status": "Success", "analysis": verdict}), 200
    except Exception as e:
        # Capture l'erreur exacte pour votre terminal
        return jsonify({"status": "Error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
