import os
import json
import google.generativeai as genai
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuration Expert Forensics (Votre clé v2O4)
GEN_KEY = "AIzaSyAJGP_etVbcz7bcBISYV7gD_kmPqaIv2O4"
genai.configure(api_key=GEN_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "DorkNetGM Sentinel - Système Actif", 200

@app.route('/health', methods=['GET'])
def health():
    # Endpoint pour le Cronjob (évite l'endormissement sur Render)
    return jsonify({"status": "online", "engine": "Quantum-Cyber"}), 200

@app.route('/api/audit', methods=['POST'])
def run_audit():
    # Récupère les données de transaction envoyées par DorkNetGM
    data = request.get_json()
    
    prompt = f"""
    En tant qu'Expert Cyber-Forensics, analyse cette transaction DorkNetGM :
    {json.dumps(data)}
    
    Détecte toute anomalie quantique ou tentative de fraude. 
    Réponds par : VERDICT (Sûr/Risqué) et RAISON.
    """
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"analysis": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
