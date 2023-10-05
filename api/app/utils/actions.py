import datetime
import json
import re
import time
from typing import Union

import requests
from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ..config import Config
from ..database import crud, models, schemas
from ..database.crud import games, rankings, time_entries, users
from . import logger
from . import my_utils as utils
from .clockify_api import ClockifyApi

clockify_api = ClockifyApi()
config = Config()


########################
##### BASIC ROUTES #####
########################


async def sync_data(db: Session, start_date: str = None, silent: bool = False):
    logger.info("Sync data...")
    start_time = time.time()
    users_db = users.get_users(db)
    logger.info("Sync clockify entries...")
    total_entries = sync_clockify_entries(db, start_date)
    if total_entries < 1:
        logger.info("No one played today")
        return
    logger.info("Updating played days...")
    for user in users_db:
        played_days = time_entries.get_played_days(db, user.id)
        users.update_played_days(db, user.id, played_days)
    logger.info("Updating played time games...")
    played_time_games = time_entries.get_games_played_time(db)
    for game in played_time_games:
        games.update_total_played_time(db, game[0], game[1])
    logger.info("Updating played time users...")
    played_time_users = time_entries.get_users_played_time(db)
    for user in played_time_users:
        users.update_played_time(db, user[0], user[1])
    logger.info("Updating played time game-user...")
    for user in users_db:
        played_time_games = time_entries.get_user_games_played_time(db, user.id)
        for game in played_time_games:
            users.update_played_time_game(db, user.id, game[0], game[1])
    await ranking_games_hours(db)
    await ranking_players_hours(db)
    # sync_played_games_user(db)
    # check_ranking_played_hours(db)
    end_time = time.time()
    logger.info("Elapsed time: " + str(end_time - start_time))


def streak_days(db: Session):
    """
    TODO: To revise
    """
    # entries = time_entries.get_time_entries(db)
    # logger.info("Total entries: " + str(entries.count()))
    # played_days = 0
    # last_played_day = 1
    # max_played_days = 0
    # last_played_date = ""
    # for entry in entries:
    #     day_of_the_year = utils.day_of_the_year(str(entry.start))
    #     if day_of_the_year == last_played_day + 1:
    #         played_days += 1
    #     else:
    #         last_played_date = utils.date_from_day_of_the_year()
    #         max_played_days = played_days
    #         played_days = 0
    #     break
    return


def sync_played_games(db: Session, start_date: str = None):
    logger.info("Sync played games (To Revise)...")
    if start_date is None:
        date = datetime.datetime.now()
        start = date - datetime.timedelta(days=1)
        start = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start = date - datetime.timedelta(days=1)
        start = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    time_entries_db = time_entries.get_time_entries(db, start_date)
    logger.info("TIMEENTRIES: " + str(len(time_entries_db)))
    for time_entry in time_entries_db:
        # already_played = crud.user_get_game(db, time_entry.user_id, time_entry.project)
        if users.get_game(db, time_entry.user_id, time_entry.project) is None:
            start_game = models.UsersGames(
                game=time_entry.project,
                user=time_entry.user,
                user_id=time_entry.user_id,
            )
            db.add(start_game)
            db.commit()
            # crud.user_add_new_game()


# def sync_played_games_user(db: Session):
#     logger.info("Sync played time on every game for users...")
#     users = crud.get_users(db)
#     for user in users:
#         games = crud.user_get_played_time_games(db, user.id)
#         for game in games:
#             crud.user_update_played_time_game(db, user.id, game[0], game[1])


####################
##### RANKINGS #####
####################


async def ranking_games_hours(db: Session):
    logger.info("Checking games ranking hours...")
    try:
        # ranking_games = rankings.get_ranking_games(db)
        most_played_games = games.get_most_played_time(db, 11)
        most_played: list[models.GamesInfo] = []
        most_played_to_check = []
        for game in most_played_games:
            most_played.append(game)
            most_played_to_check.append(game.name)
        result = rankings.get_current_ranking_games(db)
        current: list[models.GamesInfo] = []
        current_to_check = []
        for game in result:
            current.append(game)
            current_to_check.append(game.name)
        if current_to_check[:10] == most_played_to_check[:10]:
            logger.info("No changes in TOP 10 games ranking")
        else:
            logger.info("Changes in TOP 10 games ranking")
            msg = "📣📣 Actualización del ránking de juegos 📣📣\n"
            i = 0
            for game in most_played:
                if i <= 10:
                    game_name = game.name
                    time = game.played_time
                    current = game.current_ranking
                    # logger.info(game_name + " " + str(i + 1))
                    # rankings.update_current_ranking_hours_game(db, i + 1, game_name)
                    diff_raw = current - (i + 1)
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
            logger.info(msg)
    except Exception as e:
        logger.info("Error in check ranking games: " + str(e))
    logger.info("Updating ranking...")
    most_played = games.get_most_played_time(db)
    i = 1
    for game in most_played:
        rankings.update_current_ranking_hours_game(db, i, game.name)
        i += 1


async def ranking_players_hours(db: Session):
    # logger.info("TBI")
    # return
    logger.info("Ranking player hours...")
    # return
    most_played_users = users.get_most_played_time(db)
    most_played: list[models.User] = []
    most_played_to_check = []
    for player in most_played_users:
        most_played.append(player)
        most_played_to_check.append(player.name)
    result = rankings.get_current_ranking_hours_players(db)
    current: list[models.User] = []
    current_to_check = []
    for player in result:
        current.append(player)
        current_to_check.append(player.name)
    # last = dict(sorted(last, key=lambda x: x[1], reverse=True))
    if current_to_check == most_played_to_check:
        logger.info("No changes in player ranking")
    else:
        logger.info("Changes in player ranking")
        # ranking_players = db.player_played_time()
        # ranking_players = dict(
        #     sorted(ranking_players, key=lambda x: x[1], reverse=True)
        # )
        msg = "📣📣 Actualización del ránking de horas 📣📣\n"
        for i, player in enumerate(most_played_users):
            name = player.name
            # rankings.update_current_ranking_hours_user(db, i + 1, player.id)
            # db.update_last_ranking_hours(i + 1, player)
            hours = player.played_time
            if hours is None:
                hours = 0
            current = player.current_ranking_hours
            diff_raw = current - (i + 1)
            diff = str(diff_raw)
            # logger.info("Checkpoint")
            # This adds + to games that up position (positive diff has not + sign)
            if diff_raw > 0:
                diff = "+" + diff
            diff = diff.replace("+", "↑")
            diff = diff.replace("-", "↓")
            if diff != "0":
                name = "*" + name + "*"
            else:
                diff = diff.replace("0", "=")
            if diff_raw > 1:
                name = "⏫ " + name
            if diff_raw == 1:
                name = "⬆️ " + name
            if diff_raw < 0:
                name = "⬇️ " + name
            msg = (
                msg
                + str(i + 1)
                + ". "
                + name
                + ": "
                + str(utils.convert_time_to_hours(hours))
                + " ("
                + diff
                + ")"
                + "\n"
            )
            rankings.update_current_ranking_hours_user(db, i + 1, player.id)
        # if not self.silent:
        #     logger.info(msg)
        #     await utils.send_message(msg)
        logger.info(msg)


# def get_last_played_games(db: Session):
#     last_played = rankings.ranking_last_played_games(db)
#     games = []
#     games_temp = []
#     i = 1
#     for game in last_played:
#         if i == 10:
#             break
#         if game[0] not in games_temp:
#             games_temp.append(game[0])
#             games.append(game)
#             i += 1
#     return games


####################
##### CLOCKIFY #####
####################


def sync_clockify_entries(db: Session, date: str = None):
    users_db = users.get_users(db)
    if date is None:
        logger.info("Syncing last time entries...")
    else:
        logger.info("Syncing time entries from " + date + "...")
    total_entries = 0
    try:
        for user in users_db:
            entries = clockify_api.get_time_entries(user.clockify_id, date)
            total_entries += len(entries)
            time_entries.sync_clockify_entries_db(db, user, entries)
        return total_entries
    except Exception as e:
        logger.info("Error syncing clockify entries: " + str(e))
        raise e
