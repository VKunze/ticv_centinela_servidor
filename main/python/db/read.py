from main.python.db.db import query
import datetime


def get_level_data():
    stmt = "SELECT height from river_status ORDER BY date DESC LIMIT 8;"
    try:
        level_data_list = [i[0] for i in query(stmt)]
        while len(level_data_list) < 8:
            level_data_list.append(0)
        return level_data_list
    except Exception as e:
        return "ERROR ----" + str(e)
    return result


def get_rain_data(date):
    stmt = "SELECT start_date, amount " \
           "FROM registered_rain_data " \
           "WHERE " \
           "start_date > DATE(now()) - INTERVAL 9 hour AND " \
           "start_date < DATE(now()) - INTERVAL 3 hour;"
    rain_data_list = [i for i in query(stmt)]
    return clean_rain_data(rain_data_list, date)


def get_full_rain_data():
    stmt = "SELECT * " \
           "FROM registered_rain_data;"
    rain_data_list = [i for i in query(stmt)]
    return rain_data_list


def clean_rain_data(rain_data_list, date):
    data_map = {}
    for (date, amount) in rain_data_list:
        if date not in data_map:
            data_map[date] = [amount]
        else:
            data_map[date].append(amount)
    for date in list(data_map.keys()):
        data_map[date] = sum(data_map[date]) / len(data_map[date])
    rain_data_list = []
    data_map = check_no_date_missing(data_map, date)
    for date in sorted(list(data_map.keys())):
        rain_data_list.append(data_map[date])
    return rain_data_list


def check_no_date_missing(data, date):
    dates = list(data.keys())
    dates.sort()
    one_hour = datetime.timedelta(hours=1)
    if dates:
        prev_date = to_string(format_date_from_string(dates[0]) - one_hour)
        for date in dates:
            amount_missing = 0
            while format_date_from_string(date) > (
                    format_date_from_string(prev_date) + one_hour + datetime.timedelta(hours=amount_missing)):
                data[to_string(
                    format_date_from_string(prev_date) + one_hour + datetime.timedelta(hours=amount_missing))] = 0
                prev_date = to_string(format_date_from_string(prev_date) + one_hour)
            prev_date = date
        if len(list(data.keys())) > 6:
            ordered_dates = list(data.keys())
            ordered_dates.sort(reverse=True)
            for i in range(6, len(ordered_dates)):
                del data[ordered_dates[i]]
        elif len(list(data.keys())) < 6:
            ordered_dates = list(data.keys())
            ordered_dates.sort(reverse=True)
            while format_date_from_string(ordered_dates[0]) < format_date_from_string(date) - one_hour:
                ordered_dates.insert(0, to_string(format_date_from_string(ordered_dates[0]) + one_hour))
                data[ordered_dates[0] + one_hour] = 0
            while len(ordered_dates) < 6:
                new_date = ordered_dates[len(ordered_dates) - 1] - one_hour
                ordered_dates.append(to_string(new_date))
                data[to_string(new_date)] = 0
    else:
        for i in range(1, 7):
            data[to_string(date - datetime.timedelta(hours=i))] = 0
    return data


def format_date_from_string(date_string):
    date_format = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.strptime(date_string, date_format)


def to_string(date):
    date_format = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.strftime(date, date_format)
