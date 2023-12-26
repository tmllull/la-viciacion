import datetime
import json
import re
import time
from typing import Union

import requests
from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ..config import Config
from ..crud import clockify, games, rankings, time_entries, users
from ..crud.achievements import Achievements
from ..database import models, schemas
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
    if silent:
        silent = True
    start_time = time.time()
    silent = False
    if sync_all:
        start_date = config.START_DATE
        silent = True
        # config.sync_all = True
    achievements = Achievements(silent)
    clockify.sync_clockify_tags(db)
    achievements.populate_achievements(db)
    users_db = users.get_users(db)
    logger.info("Sync clockify entries...")
    for user in users_db:
        if user.name is not None and user.name != "":
            user_name = str(user.name)
        else:
            user_name = str(user.username)
        logger.info("#### " + str(user_name) + " ####")

        # Create user statistics entry (if needed)
        users.create_user_statistics(db, user.id)
        users.create_user_statistics_historical(db, user.id)

        # Update clockify_id for user if has not been set and email matches with a valid user on Clockify
        if user.clockify_id is None or not utils.check_hex(user.clockify_id):
            users.update_clockify_id(
                db, user.username, clockify_api.get_user_by_email(user.email)
            )

        # Sync time_entries from Clockify with local DB
        total_entries, entries = await utils.sync_clockify_entries(
            db, user, start_date, silent
        )
        if total_entries < 1:
            logger.info(str(user_name) + " not played in the last 24h")
            continue

        # Update some user statistics
        logger.info("Updating played days...")
        played_days = time_entries.get_played_days(db, user.id)
        users.update_played_days(db, user.id, len(played_days))
        # Check played days achievement
        achievements.user_played_total_days(db, user, len(played_days))
        logger.info("Checking streaks for " + user.name)
        best_streak_date, best_streak, current_streak = streak_days(
            db, user, played_days
        )
        await check_streaks(db, user, current_streak, best_streak, silent)
        # TODO: Check streaks achievement
        users.update_streaks(db, user.id, current_streak, best_streak, best_streak_date)

        logger.info("Updating played time games...")
        played_time_games = time_entries.get_user_games_played_time(db, user.id)
        for game in played_time_games:
            users.update_played_time_game(db, user.id, game[0], game[1])
        logger.info("Updating played time...")
        played_time = time_entries.get_user_played_time(db, user.id)
        users.update_played_time(db, user.id, played_time[1])
        # Check total played time achievements
        logger.info("Check total played time achievements...")
        achievements.user_played_total_time(db, user, played_time[1])
        # TODO: implement achievements related to entries (like h/day, sessions/day, etc)
        achievements.user_session_time(db, user)
        # Other achievements
        achievements.user_played_total_games(db, user)
        achievements.user_streak(db, user, best_streak, best_streak_date)

        # use 'entries'

    # Update some game statistics
    logger.info("Updating played time for games...")
    played_time_games = time_entries.get_games_played_time(db)
    for game in played_time_games:
        games.update_total_played_time(db, game[0], game[1])

    # Check rankings
    await ranking_games_hours(db, silent)
    await ranking_players_hours(db, silent)
    end_time = time.time()
    logger.info("Elapsed time: " + str(end_time - start_time))


# async def sync_games_from_clockify(db: Session):
#     # TODO: TBI if needed. The following code not works
#     played_games = games.get_all_played_games(db)
#     logger.info("Adding games...")
#     for game in played_games:
#         if not games.get_game_by_name(db, game[0]):
#             await games.new_game(db, game)


def streak_days(db: Session, user: models.User, played_dates: list[models.TimeEntry]):
    """
    TODO:
    """
    #    played_dates = time_entries.get_played_days(db, user.id)
    # return

    max_streak = 0
    start_streak_date = None
    end_max_streak_date = None
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
                end_max_streak_date = played_dates[i - 1]
            current_streak = 0

    # Check today to add this day to the streak
    today = datetime.date.today()
    if (today - played_dates[-1]).days == 1:
        current_streak += 1

    # Check if current streak (with today) is longer than best (without today)
    if current_streak > max_streak:
        max_streak = current_streak
        end_max_streak_date = played_dates[-1]

    # Check is there is more than 1 day without play
    if (today - played_dates[-1]).days > 1:
        current_streak = 0

    return end_max_streak_date, max_streak, current_streak


async def check_streaks(
    db: Session,
    user: models.User,
    current_streak: int,
    best_streak: int,
    silent: bool = False,
):
    hour = datetime.datetime.now().hour
    minutes = datetime.datetime.now().minute
    # Check if user lose streak
    current_db_streaks_data = users.get_streaks(db, user.id)[0]
    # logger.info(current_streaks_data[0])
    current_db_streak = current_db_streaks_data[0]
    best_db_streak = current_db_streaks_data[1]
    best_db_streak_date = current_db_streaks_data[2]
    if (
        current_db_streak is not None
        and current_streak == 0
        and current_db_streak > 10
        and hour == 5
        and minutes == 0
    ):
        msg = (
            user.name
            + " acaba de perder la racha de "
            + str(current_db_streak)
            + " días."
        )
        logger.info(msg)
        await utils.send_message(msg, silent)
    # TODO: Check this to avoid daily notifications when the streak is not lost
    # if best_db_streak is not None and best_streak > best_db_streak:
    #     msg = (
    #         user.name
    #         + " acaba de superar su mejor racha de "
    #         + str(best_db_streak)
    #         + " días."
    #     )
    #     logger.info(msg)
    #     await utils.send_message(msg, silent)


####################
##### RANKINGS #####
####################


async def ranking_games_hours(db: Session, silent: bool):
    logger.info("Checking games ranking hours...")
    try:
        msg = ""
        most_played_games = games.get_most_played_time(db, 11)
        most_played: list[models.GameStatistics] = []
        most_played_to_check = []  # Only for easy check with current ranking
        for game in most_played_games:
            most_played.append(game)
            most_played_to_check.append(game.game_id)
        result = games.current_ranking_hours(db)
        current: list[models.Game] = []
        current_to_check = []  # Only for easy check with most played
        for game in result:
            current.append(game)
            current_to_check.append(game.game_id)
        if current_to_check[:10] == most_played_to_check[:10]:
            msg = "No changes in TOP 10 games ranking"
            logger.info("No changes in TOP 10 games ranking")
        else:
            logger.info("Changes in TOP 10 games ranking")
            msg = "📣📣 Actualización del ránking de juegos 📣📣\n"
            i = 0
            for game in most_played:
                if i <= 10:
                    game_name = games.get_game_by_id(db, game.game_id).name
                    time = game.played_time
                    current = game.current_ranking
                    diff_raw = current - (i + 1)
                    diff = str(diff_raw)
                    # This adds '+' sign to games that up position (positive diff has not '+' sign)
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
            await utils.send_message(msg, silent)
            logger.info(msg)
    except Exception as e:
        logger.info("Error in check ranking games: " + str(e))
    logger.info("Updating games ranking...")
    most_played = games.get_most_played_time(db)
    i = 1
    for game in most_played:
        games.update_current_ranking_hours(db, i, game.game_id)
        i += 1


async def ranking_players_hours(db: Session, silent: bool):
    logger.info("Ranking player hours...")
    played_time_db = users.played_time(db)
    most_played: list[models.User] = []
    most_played_to_check = []  # Only for easy check with current ranking
    for player in played_time_db:
        most_played.append(player)
        most_played_to_check.append(player.user_id)
    current_ranking_db = users.current_ranking_hours(db)
    current: list[models.User] = []
    current_to_check = []  # Only for easy check with most played
    for player in current_ranking_db:
        current.append(player)
        current_to_check.append(player.user_id)
    if current_to_check == most_played_to_check:
        logger.info("No changes in player ranking")
    else:
        logger.info("Changes in player ranking")
        msg = "📣📣 Actualización del ránking de horas 📣📣\n"
        for i, player in enumerate(played_time_db):
            name = str(users.get_user_by_id(db, player.user_id).name)
            hours = player.played_time
            if hours is None:
                hours = 0
            current = player.current_ranking_hours
            diff_raw = current - (i + 1)
            diff = str(diff_raw)
            # This adds '+' sign to games that up position (positive diff has not '+' sign)
            if diff_raw > 0:
                diff = "+" + diff
            diff = diff.replace("+", "↑")
            diff = diff.replace("-", "↓")
            if diff != "0":
                name = "*" + str(name) + "*"
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
            users.update_current_ranking_hours(db, i + 1, player.user_id)
        await utils.send_message(msg, silent)
        logger.info(msg)
    logger.info("Updating players ranking...")
    current_ranking = users.current_ranking_hours(db)
    i = 1
    for user in current_ranking:
        users.update_current_ranking_hours(db, i, user.user_id)
        i += 1
