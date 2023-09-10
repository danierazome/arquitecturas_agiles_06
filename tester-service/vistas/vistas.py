from flask import request
from flask_restful import Resource
from dotenv import load_dotenv

import pika
import redis
import os

load_dotenv()


redis_client = redis.StrictRedis(
    host=os.environ.get("REDIS_ADDRESS"), port=os.environ.get("REDIS_PORT"), db=0, decode_responses=True)


class VistaIps(Resource):
    def get(self, servicio_name):
        keys = redis_client.keys(servicio_name + '*')
        ips = redis_client.mget(keys)
        return ips


class VistaServicio(Resource):

    def post(self):
        service_name_pattern = request.json['servicio_name'] + '*'
        servicios_keys = redis_client.keys(service_name_pattern)
        servicios_ip = redis_client.mget(servicios_keys)
        return {"servicios_ip": servicios_ip}


class VistaCandidato(Resource):

    def post(self):
        ip = os.environ.get("RABBITMQ_ADDRESS")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(os.environ.get("RABBITMQ_ADDRESS")))
        channel = connection.channel()

        channel.queue_declare(queue='heartbeat')

        channel.basic_publish(exchange='',
                              routing_key='s-log',
                              body=request.json['info'])

        connection.close()

        return {'mesage': 'mensage delivered', 'result': True}

    def post(self):
        ip = os.environ.get("RABBITMQ_ADDRESS")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(os.environ.get("RABBITMQ_ADDRESS")))
        channel = connection.channel()

        channel.queue_declare(queue='s-log')

        channel.basic_publish(exchange='',
                              routing_key='s-log',
                              body=request.json['info'])

        connection.close()

        return {'mesage': 'mensage delivered', 'result': True}


class VistaLog(Resource):

    def post(self):
        log_message = "holi"
        logs = open("logs.txt", "a+")  # append mode
        logs.write(log_message + "\n")
        logs.close()
        ip = os.environ.get("RABBITMQ_ADDRESS")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(os.environ.get("RABBITMQ_ADDRESS")))
        channel = connection.channel()

        channel.queue_declare(queue='s-log')

        channel.basic_publish(exchange='',
                              routing_key='s-log',
                              body=request.json['info'])

        connection.close()

        return {'mesage': 'mensage delivered', 'result': True}
