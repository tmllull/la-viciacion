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
from ..database.crud import clockify, games, rankings, time_entries, users
from . import logger
from . import my_utils as utils
from .clockify_api import ClockifyApi

clockify_api = ClockifyApi()
config = Config()


########################
##### BASIC ROUTES #####
########################


async def sync_data(
    db: Session,
    start_date: str = None,
    silent: bool = False,
    sync_all: bool = False,
):
    logger.info("Sync data...")
    start_time = time.time()
    if sync_all:
        start_date = "2023-01-01"
    clockify.sync_clockify_tags(db)
    users_db = users.get_users(db)
    logger.info("Sync clockify entries...")
    for user in users_db:
        total_entries = await sync_clockify_entries(db, user, start_date)
        if total_entries < 1:
            logger.info(user.name + " not played today")
            continue
        logger.info("Updating played days...")
        played_days = time_entries.get_played_days(db, user.id)
        users.update_played_days(db, user.id, len(played_days))
        logger.info("Updating streaks...")
        best_streak_date, best_streak, current_streak = streak_days(db, user)
        users.update_streaks(db, user.id, current_streak, best_streak, best_streak_date)
        played_time_games = time_entries.get_user_games_played_time(db, user.id)
        logger.info("Updating played time games...")
        for game in played_time_games:
            users.update_played_time_game(db, user.id, game[0], game[1])
        logger.info("Updating played time...")
        played_time = time_entries.get_user_played_time(db, user.id)
        users.update_played_time(db, user.id, played_time[1])
    logger.info("Updating played time games...")
    played_time_games = time_entries.get_games_played_time(db)
    for game in played_time_games:
        games.update_total_played_time(db, game[0], game[1])
    logger.info("Updating played time users...")
    played_time_users = time_entries.get_users_played_time(db)
    for user in played_time_users:
        users.update_played_time(db, user[0], user[1])
    await ranking_games_hours(db)
    await ranking_players_hours(db)
    end_time = time.time()
    logger.info("Elapsed time: " + str(end_time - start_time))


async def sync_games_from_clockify(db: Session):
    games_db = games.get_all_played_games(db)
    logger.info("Adding games...")
    for game in games_db:
        if not games.get_game_by_name(db, game[0]):
            await games.new_game(db, game)


def streak_days(db: Session, user: models.User):
    """
    TODO: To revise
    """
    logger.info("Checking streaks for " + user.name)
    played_dates = time_entries.get_played_days(db, user.id)
    # return

    max_streak = 0
    start_streak_date = None
    end_streak_date = None
    current_streak = 0

    for i in range(1, len(played_dates)):
        # Check diff between current and last date
        diff = (played_dates[i] - played_dates[i - 1]).days
        if diff == 1:
            if current_streak == 0:
                start_streak_date = played_dates[i - 1]
            current_streak += 1
        else:
            if current_streak > max_streak:
                max_streak = current_streak
                end_streak_date = played_dates[i - 1]
            current_streak = 0

    # Check today to add this day to the streak
    today = datetime.date.today()
    if (today - played_dates[-1]).days == 1:
        current_streak += 1

    # Check if current streak (with today) is longer than best (without today)
    if current_streak > max_streak:
        max_streak = current_streak
        end_streak_date = played_dates[-1]

    # Check is there is more than 1 day without play
    if (today - played_dates[-1]).days > 1:
        current_streak = 0

    return end_streak_date, max_streak, current_streak


####################
##### RANKINGS #####
####################


async def ranking_games_hours(db: Session):
    logger.info("Checking games ranking hours...")
    try:
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
    logger.info("Ranking player hours...")
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
    if current_to_check == most_played_to_check:
        logger.info("No changes in player ranking")
    else:
        logger.info("Changes in player ranking")
        msg = "📣📣 Actualización del ránking de horas 📣📣\n"
        for i, player in enumerate(most_played_users):
            name = player.name
            hours = player.played_time
            if hours is None:
                hours = 0
            current = player.current_ranking_hours
            diff_raw = current - (i + 1)
            diff = str(diff_raw)
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


####################
##### CLOCKIFY #####
####################


async def sync_clockify_entries(db: Session, user: models.User, date: str = None):
    try:
        entries = clockify_api.get_time_entries(user.clockify_id, date)
        total_entries = len(entries)
        logger.info(
            "Sync " + str(total_entries) + " entries for user " + str(user.name)
        )
        if total_entries == 0:
            return 0
        await time_entries.sync_clockify_entries_db(db, user, entries)
        return total_entries
    except Exception as e:
        logger.info("Error syncing clockify entries: " + str(e))
        raise e


def sync_all_clockify_entries(db: Session, date: str = None):
    users_db = users.get_users(db)
    try:
        for user in users_db:
            entries = clockify_api.get_time_entries(user.clockify_id, date)
            time_entries.sync_clockify_entries_db(db, user, entries)
    except Exception as e:
        logger.info("Error syncing clockify entries: " + str(e))
        raise e
