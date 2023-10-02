import datetime

import pytz
from dateutil.parser import isoparse


def convert_time_to_hours(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h{minutes}m"


def change_timezone_clockify(time):
    date_time = isoparse(time)
    spain_timezone = pytz.timezone("Europe/Madrid")
    return str(date_time.astimezone(spain_timezone).strftime("%Y-%m-%d %H:%M:%S"))
