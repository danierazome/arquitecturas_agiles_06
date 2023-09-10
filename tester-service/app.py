from flask_coney import Coney
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv


from vistas import VistaLog, VistaIps, redis_client


import redis
import pika
import os

load_dotenv()


# ----------> FLASK APP CONFIG
app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["CONEY_BROKER_URI"] = os.environ.get("RABBITMQ_URL_CONNECTION")


api = Api(app)

# ----------> REDIS CONFIG

api.add_resource(VistaIps, '/api/ip/<string:servicio_name>')
api.add_resource(VistaLog, '/api/ip/log')

# -------

coney = Coney(app)

# ----


@coney.queue(queue_name="hello")
def process_queue(ch, method, props, body):
    servicio_informacion = body.decode('utf-8').split(',')
    print(servicio_informacion)
    redis_client.set(servicio_informacion[0], servicio_informacion[1], ex=2)


""" class BackgroundRunner:
    def __init__(self, executor):
        self.executor = executor
        redis_client = redis.StrictRedis(
            host='localhost', port=6379, db=0, decode_responses=True)

    redis_client = redis.StrictRedis(
        host='localhost', port=6379, db=0, decode_responses=True)
    # ----------> SUSCRIPCION TOPICO REGISTRAR SERVICO

    def registrarServicio(ch, method, properties, body):
        servicio_information = body.split(",")
        redis_client.set(
            servicio_information[0], servicio_information[1], ex=2)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('172.17.0.2'))

    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_consume(queue='hello',
                          auto_ack=True,
                          on_message_callback=registrarServicio)

    channel.basic_qos(prefetch_count=1)

    channel.start_consuming() """
