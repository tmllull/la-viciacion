import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ..crud import users
from ..database import models, schemas
from ..utils import actions as actions
from ..utils import logger
from ..utils import my_utils as utils
from ..utils.clockify_api import ClockifyApi

clockify = ClockifyApi()

####################
##### RANKINGS #####
####################


def user_hours_players(db: Session, limit: int = None) -> list[models.Users]:
    try:
        stmt = (
            select(
                (models.Users.id).label("user_id"),
                models.Users.name,
                models.Users.played_time,
            )
            .order_by(desc(models.Users.played_time))
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)


def user_days_players(db: Session, limit: int = None) -> list[models.Users]:
    try:
        stmt = (
            select(
                (models.Users.id).label("user_id"),
                models.Users.name,
                models.Users.played_days,
            )
            .order_by(desc(models.Users.played_days))
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e


def user_best_streak(db: Session, limit: int = None):
    try:
        stmt = (
            select(
                (models.Users.id).label("user_id"),
                models.Users.name,
                models.Users.best_streak,
            )
            .order_by(desc(models.Users.best_streak))
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e


def user_current_streak(db: Session, limit: int = None):
    try:
        stmt = (
            select(
                (models.Users.id).label("user_id"),
                models.Users.name,
                models.Users.current_streak,
            )
            .order_by(desc(models.Users.current_streak))
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e


def user_ranking_achievements(db: Session, limit: int = None):
    return (
        db.query(
            models.UserAchievements.user_id, func.count(models.UserAchievements.user_id)
        )
        .group_by(models.UserAchievements.user_id)
        .order_by(func.count(models.UserAchievements.user_id).desc())
        .limit(limit)
    )


def user_played_games(db: Session, limit: int = None):
    try:
        stmt = (
            select(
                models.UsersGames.user_id,
                func.count(models.UsersGames.game_id).label("game_count"),
                models.Users.name,
            )
            .join(models.Users, models.Users.id == models.UsersGames.user_id)
            .group_by(models.UsersGames.user_id, models.Users.name)
            .order_by(func.count(models.UsersGames.game_id).desc())
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e


def user_completed_games(db: Session, limit: int = None):
    try:
        stmt = (
            select(
                models.UsersGames.user_id,
                models.Users.name,
                func.count(models.UsersGames.game_id),
            )
            .group_by(models.UsersGames.user_id)
            .join(models.Users, models.Users.id == models.UsersGames.user_id)
            .filter(models.UsersGames.completed == 1)
            .order_by(func.count(models.UsersGames.game_id).desc())
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e


def games_last_played(db: Session, limit: int = 10):
    try:
        stmt = (
            select(
                models.TimeEntries.project_clockify_id,
                models.GamesInfo.name,
                models.TimeEntries.start,
            )
            .join(
                models.GamesInfo,
                models.GamesInfo.clockify_id == models.TimeEntries.project_clockify_id,
            )
            .order_by(desc(models.TimeEntries.start))
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e


def user_last_played_games(db: Session, username: str, limit: int = None):
    try:
        stmt = (
            select(
                models.TimeEntries.project_clockify_id,
                models.TimeEntries.user_id,
                models.TimeEntries.start,
                models.Users.name,
            )
            .join(models.Users, models.Users.id == models.TimeEntries.user_id)
            .filter(models.Users.username == 1)
            .order_by(func.count(models.UsersGames.game_id).desc())
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e
    stmt = (
        select(
            models.TimeEntries.project_clockify_id,
            models.TimeEntries.user_id,
            models.TimeEntries.start,
        )
        .order_by(desc(models.TimeEntries.start))
        .limit(limit)
    )
    return db.execute(stmt).fetchall()


def games_most_played(db: Session, limit: int = 10):
    stmt = (
        select(models.GamesInfo.name, models.GamesInfo.played_time)
        .order_by(desc(models.GamesInfo.played_time))
        .limit(limit)
    )
    result_db = db.execute(stmt).fetchall()
    # result = {}
    # for r in result_db:
    #     result[r[0]] = r[1]
    return result_db


def platform_played_games(db: Session, limit: int = None):
    try:
        stmt = (
            select(
                (models.UsersGames.platform).label("tag_id"),
                models.ClockifyTags.name,
                func.count(models.UsersGames.platform),
            )
            .join(
                models.ClockifyTags,
                models.UsersGames.platform == models.ClockifyTags.id,
            )
            .group_by(models.UsersGames.platform)
            .order_by(func.count(models.UsersGames.platform).desc())
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e
