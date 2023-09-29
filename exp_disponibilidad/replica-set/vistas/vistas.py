from flask import request
from flask_restful import Resource

import subprocess


class VistaCandidato(Resource):

    def post(self):

        print(subprocess.run(["docker", "run", "-d", "reg-can"],
                             capture_output=True))

        return {"mensaje": "Candidato creado", "result": True}
