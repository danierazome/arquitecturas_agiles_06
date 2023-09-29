from flask import Flask
from flask_restful import Api
from flask_coney import Coney

from send_email import Email

# ----------> FLASK APP
app = Flask(__name__)

app.config["CONEY_BROKER_URI"] = 'amqp://guest:guest@172.17.0.3'
app.config['PROPAGATE_EXCEPTIONS'] = True


api = Api(app)

# -------> MESSAGE BROKER
coney = Coney(app)

email = Email()


@coney.queue(queue_name="send-email")
def process_queue(ch, method, props, body):
    log_message = body.decode('utf-8')
    print(log_message)
    email.send_email(log_message)
