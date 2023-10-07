import datetime
import json
import re

import pytz
import requests
from dateutil.parser import isoparse
from howlongtobeatpy import HowLongToBeat

from ..config import Config
from ..database import schemas
from ..utils import logger

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
    # return spain_timezone
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


async def get_new_game_info(game) -> schemas.NewGame:
    game_name = game["name"]
    project_id = game["id"]
    released = ""
    genres = ""
    steam_id = ""
    dev = ""
    avg_time = 0
    game_info = await get_game_info(game_name)
    rawg_info = game_info["rawg"]
    hltb_info = game_info["hltb"]
    game_name = rawg_info["name"]
    released = rawg_info["released"]
    if hltb_info is None:
        steam_id = 0
        dev = "-"
        avg_time = 0
    else:
        steam_id = hltb_info["profile_steam"]
        dev = hltb_info["profile_dev"]
        avg_time = hltb_info["comp_main"]
    if steam_id == 0:
        steam_id = ""
    if released is not None:
        release_date = datetime.datetime.strptime(released, "%Y-%m-%d")
        # released = datetime.datetime.strftime(release_date, "%d-%m-%Y")
    else:
        release_date = None
    genres = ""
    for genre in rawg_info["genres"]:
        genres += genre["name"] + ","
    genres = genres[:-1]
    image_url = rawg_info["background_image"]
    new_game = schemas.NewGame(
        name=game_name,
        dev=dev,
        release_date=release_date,
        steam_id=str(steam_id),
        image_url=image_url,
        genres=genres,
        avg_time=avg_time,
        clockify_id=project_id,
    )
    return new_game
