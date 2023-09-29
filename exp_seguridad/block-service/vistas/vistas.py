from flask import request
from flask_restful import Resource
from modelos import db, IntentoFallido, Candidato

from datetime import timedelta

import datetime
import pika


max_intentos_fallidos = 3

estado_activo = 1
estado_bloquedo = 2

RABBITMQ_ADDRESS = '172.17.0.3'


class VistaBloqueo(Resource):

    def post(self):

        date_now = datetime.datetime.now()

        intento_fallido = IntentoFallido(
            user_id=request.json["user_id"],
            fecha_intento=date_now
        )

        db.session.add(intento_fallido)
        db.session.commit()

        intentos = IntentoFallido.query.filter(
            IntentoFallido.user_id == request.json["user_id"],
            IntentoFallido.fecha_intento >= (date_now - timedelta(minutes=3))).all()

        if (len(intentos) < max_intentos_fallidos):
            return {"estado_bloqueo": "{} intento fallido por el usuario".format(len(intentos))}, 401

        # BLOQUEAR USUARIO
        candidato = Candidato.query.filter(
            Candidato.id == request.json["user_id"]).first()

        candidato.estado = estado_bloquedo

        db.session.add(candidato)
        db.session.commit()

        # PUBLISH EVENT TO SEND EMAIL

        print(candidato.email)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(RABBITMQ_ADDRESS))
        channel = connection.channel()

        channel.queue_declare(queue='send-email')

        channel.basic_publish(exchange='',
                              routing_key='send-email',
                              body=candidato.email)
        connection.close()

        return {"estado_bloqueo": "Usuario bloqueado"}, 423

    def delete(self):

        intentos = IntentoFallido.query.filter(
            IntentoFallido.user_id == request.json["user_id"]).all()

        for i in intentos:
            db.session.delete(i)

        db.session.commit()

        # DESBLOQUEAR USUARIO

        candidato = Candidato.query.filter(
            Candidato.id == request.json["user_id"]).first()

        candidato.estado = estado_activo

        db.session.add(candidato)
        db.session.commit()

        return {"mensaje": "Usuario limpiado"}
