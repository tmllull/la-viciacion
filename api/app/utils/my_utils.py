import datetime
import re

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


def convert_clockify_duration(duration):
    match = re.match(r"PT(\d+H)?(\d+M)?", duration)
    if match:
        horas_str = match.group(1)
        minutos_str = match.group(2)

        horas = int(horas_str[:-1]) if horas_str else 0
        minutos = int(minutos_str[:-1]) if minutos_str else 0

        # Convertir horas y minutos a segundos
        segundos = horas * 3600 + minutos * 60

        return segundos
    else:
        return 0
