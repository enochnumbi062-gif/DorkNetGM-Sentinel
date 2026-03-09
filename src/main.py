import os
import json
import requests
import google.generativeai as genai
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- CONFIGURATION EXPERT (ROOT) ---
# Correction Erreur 404 : Utilisation directe du modèle stable
GEN_KEY = "AIzaSyAJGP_etVbcz7bcBISYV7gD_kmPqaIv2O4"
genai.configure(api_key=GEN_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Identifiants Telegram vérifiés
TELEGRAM_TOKEN = "8462494984:AAGs7FHpV7QWsxatcKuVgaTaB9vwLHjyYww"
TELEGRAM_CHAT_ID = "768138087"

def send_critical_alert(msg):
    """Envoie un rapport d'alerte immédiat sur Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": f"🚨 [SENTINEL-ALERT]\n{msg}",
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

# --- LOGIQUE DE SÉCURITÉ DORKNET-GM ---

def valider_paiement_securise(transaction_data):
    """Greffe de sécurité Cyber-Quantique pour transactions"""
    prompt = f"""
    [EXPERT CYBER-FORENSICS]
    TYPE : Live-Payment-Security | ORIGIN : DorkNetGM-Mobile-Core
    TRANSACTION DATA : {json.dumps(transaction_data, indent=2)}
    
    MISSION : Analyser cette transaction. Si elle semble frauduleuse, 
    réponds par 'BLOQUER'. Sinon, donne ton feu vert.
    """
    try:
        response = model.generate_content(prompt)
        analysis = response.text.upper()
        
        # Déclenchement automatique d'alerte si suspect
        if any(word in analysis for word in ["RISQUÉ", "FRAUDE", "DANGER", "BLOQUER"]):
            return False, response.text
        return True, response.text
    except Exception as e:
        return False, f"Erreur IA : {str(e)}"

# --- ROUTES API ---

@app.route('/')
def home():
    return "DorkNetGM Quantum Sentinel Hub - Systèmes & Paiements Actifs", 200

@app.route('/health', methods=['GET'])
def health():
    # Ping pour Cronjob (Anti-Sleep Render)
    return jsonify({"status": "online", "engine": "Quantum-Cyber", "platform": "Multi-Platform"}), 200

@app.route('/api/audit', methods=['POST'])
def run_audit():
    """Endpoint pour Kali Linux et audits systèmes"""
    data = request.get_json()
    origin = data.get("origin", "Unknown Source")
    audit_type = data.get("type", "General Audit")
    
    prompt = f"""
    [EXPERT CYBER-FORENSICS]
    CONTEXTE : {origin} | TYPE : {audit_type}
    DONNÉES BRUTES : {json.dumps(data, indent=2)}
    
    MISSION : Analyser l'intégrité et donner un VERDICT (Sûr ou Risqué).
    """
    try:
        response = model.generate_content(prompt)
        verdict_text = response.text
        
        # Alerte Telegram automatique en cas de risque détecté
        if any(word in verdict_text.upper() for word in ["RISQUÉ", "DANGER", "FRAUDE"]):
            send_critical_alert(f"Menace sur {origin} !\n\n{verdict_text[:300]}")

        return jsonify({
            "status": "Success",
            "analysis": verdict_text
        }), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route('/api/pay-check', methods=['POST'])
def api_pay_check():
    """Route spécifique pour l'application DorkNetGM"""
    data = request.get_json()
    autorise, message = valider_paiement_securise(data)
    
    return jsonify({
        "authorized": autorise,
        "security_analysis": message
    }), 200 if autorise else 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
