from flask import request
from flask import g

from main.python.app_utils.app_factory import create_app
from main.python.mqtt_connection.handle_message import incoming_message
from main.python.db.save import register_weather_data


app, mqtt, mail = create_app()


@app.route('/register_data', methods=['POST', 'OPTIONS'])
def register_data():
    print("request arrived: ", request.data)
    return register_weather_data(request.data)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    with app.app_context():
        res = incoming_message(message.payload.decode())
        print(res)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
