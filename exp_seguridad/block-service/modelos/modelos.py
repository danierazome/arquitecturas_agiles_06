from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Candidato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(60))
    password = db.Column(db.String(60))
    nombre = db.Column(db.String(60))
    experiencia = db.Column(db.String(60))
    telefono = db.Column(db.String(60))
    email = db.Column(db.String(60))
    estado = db.Column(db.Integer)


class IntentoFallido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    fecha_intento = db.Column(db.Date)
