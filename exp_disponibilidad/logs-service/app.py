from flask_coney import Coney
from flask import Flask
from flask_restful import Api
from dotenv import dotenv_values

# ----------> FLASK APP
app = Flask(__name__)


# ----------> CONFIG

config = dotenv_values(".env")

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["CONEY_BROKER_URI"] = config['RABBITMQ_URL_CONNECTION']

# -------> API
api = Api(app)

# -------> MESSAGE BROKER
coney = Coney(app)


@coney.queue(queue_name="s-log")
def process_queue(ch, method, props, body):
    log_message = body.decode('utf-8')
    logs = open("logs.txt", "a+")
    logs.write(log_message + "\n")
    logs.close()
