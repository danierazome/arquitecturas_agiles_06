from flask import request
from flask_restful import Resource
from dotenv import dotenv_values

import redis

config = dotenv_values(".env")


redis_client = redis.StrictRedis(
    host=config['REDIS_ADDRESS'], port=config['REDIS_PORT'], db=0, decode_responses=True)


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
