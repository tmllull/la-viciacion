import datetime

import pytz
from dateutil.parser import isoparse


def convert_time_to_hours(seconds) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h{minutes}m"


def convert_hours_minutes_to_seconds(time) -> int:
    if time is None:
        return 0
    return time * 3600


def change_timezone_clockify(time) -> str:
    date_time = isoparse(time)
    spain_timezone = pytz.timezone("Europe/Madrid")
    return str(date_time.astimezone(spain_timezone).strftime("%Y-%m-%d %H:%M:%S"))
