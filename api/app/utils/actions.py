import datetime
import json
import re
from typing import Union

import requests
from howlongtobeatpy import HowLongToBeat
from sqlalchemy.orm import Session

from ..config import Config
from ..database import crud
from . import logger
from . import my_utils as utils
from .clockify_api import ClockifyApi

clockify = ClockifyApi()
config = Config(False)

rawgio_search_game = (
    "https://api.rawg.io/api/games?key=bc7e0ee53f654393835ad0fa3b23a8cf&page=1&search="
)

########################
##### BASIC ROUTES #####
########################


async def init_data(db: Session):
    logger.info("Init data...")
    sync_clockify_entries(db, "2023-01-01")
    await sync_games_from_clockify(db)
    init_played_time_games(db)
    init_played_time_users(db)
    return


async def sync_data(db: Session, date: str = None):
    logger.info("Sync data...")
    # sync_clockify_entries(db, date)
    # logger.info("Updating played time games...")
    # played_time_games = crud.total_played_time_games(db)
    # for game in played_time_games:
    #     crud.update_total_played_game(db, game[0], game[1])
    # await ranking_games_hours(db)
    # sync_played_games(db)
    sync_played_games_user(db)
    # check_ranking_played_hours(db)
    return


#################
##### USERS #####
#################


# def get_user_id(db: Session, user_id: Union[int, str]):
#     db_user = crud.get_user_by_tg_id(db, telegram_id=user_id)
#     if db_user is None:
#         db_user = crud.get_user_by_tg_username(db, telegram_username=user_id)
#         if db_user is None:
#             return None
#     return db_user.id


def check_rankings(db: Session):
    sync_clockify_entries(db, "2023-01-01")
    return


async def sync_games_from_clockify(db: Session):
    games = crud.get_all_played_games(db)
    logger.info("Adding games...")
    for game in games:
        if not crud.game_exists(db, game[0]):
            await add_new_game(db, game)


def init_played_time_games(db: Session):
    logger.info("Updating played time games...")
    played_time_games = crud.total_played_time_games(db)
    for game in played_time_games:
        crud.update_total_played_game(db, game[0], game[1])
    most_played_games = crud.most_played_games_time(db)
    for i, game in enumerate(most_played_games):
        crud.update_current_ranking_hours_game(db, i + 1, game[0])
        crud.update_last_ranking_hours_game(db, i + 1, game[0])


def init_played_time_users(db: Session):
    logger.info("Updating played time players...")
    most_played_users = crud.user_played_time(db)
    for i, player in enumerate(most_played_users):
        logger.info(str(i) + ": " + player[0])
        crud.update_current_ranking_hours_user(db, i + 1, player[0])
        crud.update_last_ranking_hours_user(db, i + 1, player[0])


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
            utils.convert_hours_minutes_to_seconds(hltb_main_story),
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


def sync_played_games(db: Session):
    time_entries = crud.get_all_time_entries(db)
    for time_entry in time_entries:
        logger.info(time_entry.user)
        break


def sync_played_games_user(db: Session):
    users = crud.get_users(db)
    for user in users:
        games = crud.user_played_time_game(db, user.id)
        for game in games:
            game = game[0]
            time = game[1]
            user_id = user.id
            crud.update_user_played_time_game(db, user_id, game, time)


####################
##### RANKINGS #####
####################


async def ranking_games_hours(db: Session):
    logger.info("Checking games ranking hours...")
    try:
        ranking_games = crud.get_ranking_games(db)
        if not config.silent:
            result = crud.get_current_ranking_games(db)
            current = []
            for game in result:
                current.append(game[0])
            result = crud.get_last_ranking_games(db)
            last = []
            for game in result:
                last.append(game[0])
            if current[:10] == last[:10]:
                logger.info("No changes in games ranking")
            else:
                logger.info("Changes in games ranking")
                # logger.info("CURRENT")
                # logger.info(current)
                # logger.info("LAST")
                # logger.info(last)
                msg = "📣📣 Actualización del ránking de juegos 📣📣\n"
                i = 0
                for game in ranking_games:
                    if i <= 10:
                        game_name = game[0]
                        time = game[1]
                        last = game[2]
                        current = game[3]
                        logger.info(game_name + " " + str(i + 1))
                        crud.update_last_ranking_hours_game(db, i + 1, game_name)
                        diff_raw = last - current
                        diff = str(diff_raw)
                        # This adds + to games that up position (positive diff has not + sign)
                        if diff_raw > 0:
                            diff = "+" + diff
                        diff = diff.replace("+", "↑")
                        diff = diff.replace("-", "↓")
                        if diff != "0":
                            game_name = "*" + game_name + "*"
                        else:
                            diff = diff.replace("0", "=")
                        if diff_raw > 1:
                            game_name = "⏫ " + game_name
                        if diff_raw == 1:
                            game_name = "⬆️ " + game_name
                        if diff_raw < 0:
                            game_name = "⬇️ " + game_name
                        # Only to check if game has fall of the top10
                        # Then, always break
                        if i == 10 and "↓" in diff:
                            msg = msg + "----------\n"
                            msg = (
                                msg
                                + str(i + 1)
                                + ". "
                                + game_name
                                + ": "
                                + str(utils.convert_time_to_hours(time))
                                + " ("
                                + "💀"
                                + ")"
                                + "\n"
                            )
                            break
                        elif i < 10:
                            msg = (
                                msg
                                + str(i + 1)
                                + ". "
                                + game_name
                                + ": "
                                + str(utils.convert_time_to_hours(time))
                                + " ("
                                + diff
                                + ")"
                                + "\n"
                            )
                        if i == 10:
                            break
                    i += 1

                # if not config.silent:
                #     await utils.send_message(msg)
    except Exception as e:
        logger.info("Error in check ranking games: " + str(e))
    logger.info("Sync current ranking with last ranking...")
    ranking_games = crud.get_ranking_games(db)
    i = 1
    for game in ranking_games:
        crud.update_last_ranking_hours_game(db, i, game[0])
        i += 1


def get_last_played_games(db: Session):
    last_played = crud.ranking_last_played_games(db)
    games = []
    games_temp = []
    i = 1
    for game in last_played:
        if i == 10:
            break
        if game[0] not in games_temp:
            games_temp.append(game[0])
            games.append(game)
            i += 1
    return games


####################
##### CLOCKIFY #####
####################


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
