import json
import datetime

from flask import current_app
from main.python.db.save import save_level_data
from main.python.services.external_alerts import alert_flood, alert_rain
from main.python.services.machine_learning import predict


def incoming_message(data):
    app = current_app
    try:
        m_in = json.loads(data)
        kit_id = m_in["kitId"]
        date = format_date_from_epoch(m_in["epoch"])
        height = m_in["height"] / 100
        is_raining = m_in["is_raining"]
    except:
        return ""

    res = ""
    if kit_id == 1:
        with app.app_context():
            predicted_result = predict(date, height)
            if predicted_result == 1:
                res += alert_flood() + str("\n")
            res += save_level_data(kit_id, date, height)
            if is_raining == 1:
                alert_rain()
    else:
        res += "not registered kit id"
    return res


def format_date_from_epoch(epoch):
    return datetime.datetime.fromtimestamp(epoch)
