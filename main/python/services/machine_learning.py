import model.neural_network_training as mlt
from main.python.db.read import *


def predict(date, height):
    inputs = get_data(date, height)
    if height > 9.63:
        response = 1
    else:
        response = 0
    #current_model = mlt.load_model()
    #response = mlt.single_prediction(current_model, inputs)
    return response


def get_data(date, height):
    level_data = get_level_data()
    rain_data = get_rain_data(date)
    try:
        inputs = level_data
        inputs.append(height)
        inputs.extend(rain_data)
    except Exception as e:
        print(str(e))
    return inputs