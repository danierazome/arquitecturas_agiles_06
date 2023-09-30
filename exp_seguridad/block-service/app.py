from flask import Flask
from flask_restful import Api

from modelos import db

from vistas import VistaBloqueo


# ----------> FLASK APP
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/arquitectura'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


db.init_app(app)

api = Api(app)
api.add_resource(VistaBloqueo, '/api/intento-fallido')
