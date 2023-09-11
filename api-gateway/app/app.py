from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)


registry_service_url = os.getenv("REGISTRY_HOST", "localhost") + ":3000/api/ip"

@app.route('/register', methods=['POST'])
def register_candidate():
   
    if not request.is_json:
        return jsonify({'error': 'La solicitud debe ser un JSON'}), 400

    data = request.get_json()
    
    # Realiza una solicitud GET al servicio de Registry Service para obtener las IPs activas
    try:
        response = requests.get(f'http://{registry_service_url}/reg-can')
        response.raise_for_status()

        print(response)
        active_ips = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error al obtener las IPs activas: {str(e)}'}), 500

    print(active_ips)
    # simplemente usaremos la primera IP de la lista (esto debe mejorarse)
    if active_ips:
        print(f'http://{active_ips[0]}/sign-up')
        registration_service = f'http://{active_ips[0]}/sign-up'
        response = requests.post(registration_service, json=data)
        return response.json(), response.status_code
    else:
        return jsonify({'error': 'No hay IPs activas disponibles para registry_candidate'}), 500

if __name__ == '__main__':
    app.run(debug=True)

