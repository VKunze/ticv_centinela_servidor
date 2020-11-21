from flask import Flask
from main.python.db.db import get_db
from flask_mail import Mail, Message
from flask_mqtt import Mqtt


def create_app():
    app = Flask(__name__)
    app.config.from_object('main.python.config.config')
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

    mqtt = Mqtt(app)
    mail = Mail(app)

    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        print("connected!")
        mqtt.subscribe('kitiot/centinela_datos')

    with app.app_context():
        get_db()

    return app, mqtt, mail
