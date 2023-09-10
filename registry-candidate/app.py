from flask import Flask
from flask_restful import Api

from dotenv import dotenv_values

from modelos import db
from vistas import VistaCandidato
from heartbeat_job import heartbeat_thread

# ---->
app = Flask(__name__)

# -----> CONFIGURACIONES

config = dotenv_values(".env")

app.config['SQLALCHEMY_DATABASE_URI'] = config['POSTGRES_URL_CONNECTION']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# -----> INICIAR DB

db.init_app(app)

# ----> APIS
api = Api(app)

api.add_resource(VistaCandidato, '/sign-up')

# ----> INICIALIZAR HEARTBEAT THREAD

heartbeat_thread.start()
