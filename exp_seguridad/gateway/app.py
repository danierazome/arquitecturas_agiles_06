from flask import Flask
from flask_restful import Api

from vistas import VistaLoginCandidato, VistaLoginEmpleado, VistaCandidato


# ----------> FLASK APP
app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
api.add_resource(VistaLoginCandidato, '/api/login-candidato')
api.add_resource(VistaLoginEmpleado, '/api/login-empleado')

api.add_resource(VistaCandidato, '/api/candidato')
