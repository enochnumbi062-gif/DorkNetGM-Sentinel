import os
import google.generativeai as genai
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- CONFIGURATION SÉCURISÉE ---
GEN_KEY = "AIzaSyAJGP_etVbcz7bcBISYV7gD_kmPqaIv2O4"
genai.configure(api_key=GEN_KEY)

# Initialisation du modèle STABLE uniquement
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/api/audit', methods=['POST'])
def run_audit():
    try:
        data = request.get_json()
        # Appel direct sans spécifier de version d'API
        response = model.generate_content("Analyse de sécurité : " + str(data))
        return jsonify({"status": "Success", "analysis": response.text}), 200
    except Exception as e:
        # Renvoie l'erreur réelle pour qu'on puisse la voir sur Kali
        return jsonify({"status": "Error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
