from flask import request
from flask_restful import Resource
from modelos import db, Candidato


estado_bloquedo = 2


class VistaCandidato(Resource):
    def get(self):

        candidato = Candidato.query.filter(
            Candidato.id == request.json['user_id']).first()

        if candidato == None:
            return {"mensaje": "Usuario no encontrado"}, 404

        response = {}
        response["nombre"] = candidato.nombre
        response["experiencia"] = candidato.experiencia
        response["telefono"] = candidato.telefono

        return response

    def put(self):

        candidato = Candidato.query.filter(
            Candidato.id == request.json['user_id']).first()

        if candidato == None:
            return {"mensaje": "Usuario no encontrado"}, 404

        candidato.nombre = request.json['nombre']
        candidato.experiencia = request.json['experiencia']
        candidato.telefono = request.json['telefono']

        db.session.add(candidato)
        db.session.commit()

        return {"mensaje": "Usuario editado exitosamente"}
