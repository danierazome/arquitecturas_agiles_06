from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt


class VistaGenerar(Resource):
    def post(self):

        token_claims = {"id": request.json['user_id'],
                        "roles": request.json['roles']}

        token_de_acceso = create_access_token(token_claims)

        return {"token": token_de_acceso}


class VistaValidar(Resource):

    @jwt_required()
    def post(self):
        claims = get_jwt()

        tiene_role = [r for r in claims["sub"]
                      ["roles"] if r in request.json['roles']]

        if len(tiene_role) > 0:
            return {"user_id": claims["sub"]["id"]}

        return {"mensaje": "No autorizado"}, 403
