from flask import request
from flask_restful import Resource
from modelos import db, Candidato, Empleado
from roles import Role

import requests

estado_activo = 1
estado_bloquedo = 2


class VistaLoginCandidato(Resource):
    def post(self):

        candidato = Candidato.query.filter(
            Candidato.usuario == request.json['usuario']).first()

        if candidato == None:
            return {"mensaje": "Usuario no registrado"}, 404

        if candidato.estado == estado_bloquedo:
            return {"mensaje": "Usuario se encuentra bloqueado por 24 horas"}, 423

        if candidato.password == request.json['password']:
            roles = [Role.CANDIDATO.value]
            response_generar_token = requests.post(
                url='http://localhost:5002/api/generar-token',
                json={"user_id": candidato.id, "roles": roles})

            return response_generar_token.json()

        response_block_service = requests.post(
            url='http://localhost:5000/api/intento-fallido', json={"user_id": candidato.id})

        return response_block_service.json(), response_block_service.status_code


class VistaLoginEmpleado(Resource):
    def post(self):

        empleado = Empleado.query.filter(
            Empleado.usuario == request.json['usuario']).first()

        if empleado == None:
            return {"mensaje": "Usuario no registrado"}, 404

        if empleado.password != request.json['password']:
            return {"mensaje": "password incorrecto"}, 400

        roles = [Role.EMPLEADO.value]
        response_generar_token = requests.post(
            url='http://localhost:5002/api/generar-token',
            json={"user_id": empleado.id, "roles": roles})

        return response_generar_token.json()
