from flask_coney import Coney
from flask import Flask
from flask_restful import Api
from dotenv import dotenv_values

from vistas import VistaIps, redis_client


# ----------> FLASK APP
app = Flask(__name__)

# ----------> CONFIG
config = dotenv_values(".env")

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["CONEY_BROKER_URI"] = config['RABBITMQ_URL_CONNECTION']


api = Api(app)

# ----------> REDIS CONFIG

api.add_resource(VistaIps, '/api/ip/<string:servicio_name>')

# -------

coney = Coney(app)


@coney.queue(queue_name="heartbeat")
def process_queue(ch, method, props, body):
    servicio_informacion = body.decode('utf-8').split(',')
    print(servicio_informacion)
    redis_client.set(servicio_informacion[0], servicio_informacion[1], ex=4)
