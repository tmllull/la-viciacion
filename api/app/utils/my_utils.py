import datetime
import json
import re

import pytz
import requests
from dateutil.parser import isoparse
from howlongtobeatpy import HowLongToBeat

from ..config import Config

config = Config()


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


def day_of_the_year(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Obtiene el día numérico del año
    return date.timetuple().tm_yday


def date_from_day_of_the_year(day):
    start_date = datetime.datetime(2023, 1, 1)
    current_date = start_date + datetime.timedelta(days=day - 1)

    # Obtiene el día numérico del año
    return current_date.strftime("%Y-%m-%d")


def date_from_datetime(datetime: str):
    return datetime.split(" ")[0]


async def get_game_info(game):
    # Rawg
    game_request = requests.get(config.RAWG_URL + game)
    try:
        rawg_content = json.loads(game_request.content)["results"][0]
    except Exception:
        rawg_content = None
    # HLTB
    game = game.replace(":", "")
    game = game.replace("/", "")
    results_list = await HowLongToBeat().async_search(game)
    if results_list is not None and len(results_list) > 0:
        best_element = max(results_list, key=lambda element: element.similarity)
        hltb_content = best_element.json_content
    else:
        hltb_content = None

    return {"rawg": rawg_content, "hltb": hltb_content}
