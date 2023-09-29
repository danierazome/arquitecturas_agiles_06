from threading import Thread
from dotenv import dotenv_values

import pika
import uuid
import socket
import time

config = dotenv_values(".env")
app_id = config['APP_NAME'] + str(uuid.uuid4())


def sendHeartbeat():
    while True:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        url = "".join([ip_address, ':', '5000'])

        evento = "".join([app_id, ',', url])

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(config['RABBITMQ_ADDRESS']))
        channel = connection.channel()

        channel.queue_declare(queue='heartbeat')

        channel.basic_publish(exchange='',
                              routing_key='heartbeat',
                              body=evento)
        connection.close()
        time.sleep(4)


def printIp():
    while True:

        time.sleep(5)


heartbeat_thread = Thread(target=sendHeartbeat)
