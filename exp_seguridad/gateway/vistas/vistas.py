from flask import request
from flask_restful import Resource
from roles import Role

import requests


class VistaLoginCandidato(Resource):
    def post(self):

        response_login = requests.post(
            url='http://localhost:5001/api/login-candidato',
            json=request.json)

        return response_login.json(), response_login.status_code


class VistaLoginEmpleado(Resource):
    def post(self):

        response_login = requests.post(
            url='http://localhost:5001/api/login-empleado',
            json=request.json)

        return response_login.json(), response_login.status_code


class VistaCandidato(Resource):
    def get(self):

        roles = [Role.CANDIDATO.value]

        response_validar_token = requests.post(
            url='http://localhost:5002/api/validar-token',
            json={"roles": roles}, headers={"Authorization": request.headers['Authorization']})

        if response_validar_token.status_code != 200:
            return response_validar_token.json(), response_validar_token.status_code

        response_candidato = requests.get(
            url='http://localhost:5003/api/candidato',
            json=response_validar_token.json())

        return response_candidato.json(), response_candidato.status_code

    def put(self):

        roles = [Role.CANDIDATO.value]

        response_validar_token = requests.post(
            url='http://localhost:5002/api/validar-token',
            json={"roles": roles},
            headers={"Authorization": request.headers['Authorization']})

        if response_validar_token.status_code != 200:
            return response_validar_token.json(), response_validar_token.status_code

        request.json['user_id'] = response_validar_token.json()['user_id']

        response_candidato = requests.put(
            url='http://localhost:5003/api/candidato',
            json=request.json)

        return response_candidato.json(), response_candidato.status_code
