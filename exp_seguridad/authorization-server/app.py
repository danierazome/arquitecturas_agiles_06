from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from vistas import VistaGenerar, VistaValidar

# ----------> FLASK APP
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True


api = Api(app)
api.add_resource(VistaGenerar, '/api/generar-token')
api.add_resource(VistaValidar, '/api/validar-token')

jwt = JWTManager(app)
