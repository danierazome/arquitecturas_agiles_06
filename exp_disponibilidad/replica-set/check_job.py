from threading import Thread
from dotenv import dotenv_values
from datetime import datetime

import pika
import time
import redis
import subprocess

config = dotenv_values(".env")
reg_candidate_name = config['APP_NAME']

redis_client = redis.StrictRedis(
    host=config['REDIS_ADDRESS'], port=config['REDIS_PORT'], db=0, decode_responses=True)


def sendHeartbeat():
    while True:
        keys = redis_client.keys(reg_candidate_name + '*')
        ips = redis_client.mget(keys)

        if len(ips) == 2:
            print("equal")
            time.sleep(4)
            continue

        # GENERAR EVENTO PARA REGISTRAR LOG ERROR
        event_date = datetime.now()

        evento = 'ERROR' + '-' + \
            str(event_date) + '-' + reg_candidate_name + '-' + 'Falta instancia'

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(config['RABBITMQ_ADDRESS']))
        channel = connection.channel()

        channel.queue_declare(queue='s-log')

        channel.basic_publish(exchange='',
                              routing_key='s-log',
                              body=evento)

        # GENERAR EVENTO PARA REGISTRAR LOG INFORMACION

        print(subprocess.run(["docker", "run", "-d", "reg-can"],
                             capture_output=True))

        evento_debug = 'DEBUG' + '-' + \
            str(event_date) + '-' + reg_candidate_name + \
            '-' + 'Instancia inicializada'

        channel.basic_publish(exchange='',
                              routing_key='s-log',
                              body=evento_debug)
        print('different')
        connection.close()
        time.sleep(4)


heartbeat_thread = Thread(target=sendHeartbeat)
