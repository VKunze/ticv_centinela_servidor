import json
from main.python.db.db import query
import datetime


def register_weather_data(json_data):
    try:
        name, ci, start_date, end_date, amount = validate_weather_data(json_data)
    except Exception as e:
        return "Parsing error: " + str(e)
    insert_stmt = "INSERT INTO registered_rain_data(name, ci, start_date, end_date, amount) VALUES (%s, %s, %s, %s, %s)"
    start_date = format_date_from_string(start_date)
    end_date = format_date_from_string(end_date)

    time_passed = end_date - start_date
    days, seconds = time_passed.days, time_passed.seconds
    hours = days * 24 + seconds // 3600
    rain_per_hour = amount / hours
    for i in range(0, hours+1):
        hour = start_date.hour+i if start_date.hour+i < 24 else (start_date.hour+i) % 24
        new_date = start_date.replace(hour=hour, minute=0, second=0)
        save_data(insert_stmt, (name, ci, new_date, end_date, rain_per_hour))
    return "Saved data"


def save_level_data(kit_id, date, height):
    insert_stmt = "INSERT INTO river_status(kitId, date, height) VALUES (%s, %s, %s)"
    return save_data(insert_stmt, (kit_id, date, height))


def save_data(insert_stmt, data):
    try:
        query(insert_stmt, data)
        return "La inserción de datos fue exitosa"
    except Exception as e:
        return "ERROR ----" + str(e)


def validate_weather_data(data):
    json_data = json.loads(data)

    name = json_data["name"]
    ci = json_data["ci"]
    start_date = json_data["start_date"]
    end_date = json_data["end_date"]
    amount = json_data["amount"]
    return name, ci, start_date, end_date, amount


def format_date_from_string(date_string):
    date_format = "%Y/%m/%d %H:%M"
    return datetime.datetime.strptime(date_string, date_format)
