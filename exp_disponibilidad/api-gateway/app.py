from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)


registry_service_url = '172.17.0.6:5000'


@app.route('/register', methods=['POST'])
def register_candidate():

    if not request.is_json:
        return jsonify({'error': 'La solicitud debe ser un JSON'}), 400

    data = request.get_json()

    # Realiza una solicitud GET al servicio de Registry Service para obtener las IPs activas
    try:
        response = requests.get(
            f'http://{registry_service_url}/api/ip/reg-can')
        response.raise_for_status()

        print(response)
        active_ips = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error al obtener las IPs activas: {str(e)}'}), 500

    for ip in active_ips:
        registration_service = f'http://{ip}/sign-up'
        try:
            response = requests.post(registration_service, json=data)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            continue

    return jsonify({'error': 'No se pudo registrar en ninguna IP activa'}), 500


if __name__ == '__main__':
    app.run(debug=True)
