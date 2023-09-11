from flask import Flask
from flask_restful import Api

from dotenv import dotenv_values

from vistas import VistaCandidato
from check_job import heartbeat_thread

# ---->
app = Flask(__name__)

# -----> CONFIGURACIONES

config = dotenv_values(".env")

app.config['PROPAGATE_EXCEPTIONS'] = True

# ----> APIS
api = Api(app)

api.add_resource(VistaCandidato, '/sign-up')

# ----> INICIALIZAR HEARTBEAT THREAD

heartbeat_thread.start()
