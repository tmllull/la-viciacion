import datetime
import json
import re

import requests
from howlongtobeatpy import HowLongToBeat
from sqlalchemy.orm import Session

from ..database import crud
from . import logger
from .clockify_api import ClockifyApi

clockify = ClockifyApi()

rawgio_search_game = (
    "https://api.rawg.io/api/games?key=bc7e0ee53f654393835ad0fa3b23a8cf&page=1&search="
)


async def init_data(db: Session):
    logger.info("Init data...")
    # sync_clockify_entries(db, "2023-01-01")
    # games = crud.get_all_played_games(db)
    # logger.info("Adding games...")
    # for game in games:
    #     if not crud.game_exists(db, game[0]):
    #         await add_new_game(db, game)
    logger.info("Updating played time games")
    played_time_games = crud.total_played_time_games(db)
    for game in played_time_games:
        # logger.info(game)
        crud.update_total_played_game(db, game[0], game[1])
    return


def sync_data(db: Session, date: str = None):
    # sync_clockify_entries(db, date)
    check_ranking_played_hours(db)
    return


def check_rankings(db: Session):
    sync_clockify_entries(db, "2023-01-01")
    return


def check_ranking_played_hours(db: Session):
    result = crud.user_played_time(db)
    for data in result:
        logger.info(data)
    return


def check_ranking_played_games(db: Session):
    return


def check_ranking_completed_games(db: Session):
    return


def check_streaks(db: Session):
    return


def update_played_days(db: Session):
    return


async def add_new_game(db: Session, game):
    try:
        logger.info("Adding game " + game[0])
        game_name = game[0]
        project_id = game[1]
        released = ""
        genres = ""
        steam_id = ""
        rawg_info, hltb_info, hltb_main_story = await get_game_info(game_name)
        if rawg_info is not None:
            try:
                steam_id = hltb_info["profile_steam"]
            except Exception:
                steam_id = ""
            if rawg_info["released"] is not None:
                released = datetime.datetime.strptime(
                    rawg_info["released"], "%Y-%m-%d"
                ).date()
            else:
                released = None
            for genre in rawg_info["genres"]:
                genres += genre["name"] + ","
            genres = genres[:-1]

        dev = ""
        picture_url = rawg_info["background_image"]
        if hltb_info is not None:
            dev = hltb_info["profile_dev"]
        total_games = crud.add_new_game(
            db,
            game_name,
            dev,
            steam_id,
            released,
            genres,
            hltb_main_story,
            project_id,
            picture_url,
        )
        # clockify_project = clockify.add_project(game)
        # logger.info(clockify_project)
    except Exception as e:
        if "Duplicate" not in str(e):
            logger.exception(e)


async def get_game_info(game):
    # Rawg
    game_request = requests.get(rawgio_search_game + game)
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
        hltb_content, hltb_main_history = (
            best_element.json_content,
            best_element.main_story,
        )
    else:
        hltb_content = hltb_main_history = None

    return rawg_content, hltb_content, hltb_main_history


def sync_clockify_entries(db: Session, date: str = None):
    users = crud.get_users(db)
    if date is None:
        logger.info("Syncing last time entries...")
    else:
        logger.info("Syncing time entries from " + date + "...")
    try:
        for user in users:
            entries = clockify.get_time_entries(user.clockify_id, date)
            crud.sync_clockify_entries(db, user.id, entries)
    except Exception as e:
        logger.info("Error syncing clockify entries: " + str(e))
        raise e


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
