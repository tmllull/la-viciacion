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


def user_hours_players(db: Session, limit: int = None) -> list[models.User]:
    try:
        stmt = (
            select(
                (models.User.id).label("user_id"),
                models.User.name,
                models.UserStatistics.played_time,
            )
            .join(
                models.UserStatistics, models.User.id == models.UserStatistics.user_id
            )
            .order_by(desc(models.UserStatistics.played_time))
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)


def user_days_played(db: Session, limit: int = None) -> list[models.User]:
    try:
        stmt = (
            select(
                (models.User.id).label("user_id"),
                models.User.name,
                models.UserStatistics.played_days,
            )
            .join(
                models.UserStatistics, models.User.id == models.UserStatistics.user_id
            )
            # .group_by(models.User.id, models.User.name)
            .order_by(desc(models.UserStatistics.played_days))
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info("Error getting user days player: " + str(e))
        raise e


def user_best_streak(db: Session, limit: int = None):
    try:
        stmt = (
            select(
                (models.User.id).label("user_id"),
                models.User.name,
                models.UserStatistics.best_streak,
                models.UserStatistics.best_streak_date,
            )
            .join(
                models.UserStatistics, models.User.id == models.UserStatistics.user_id
            )
            # .group_by(models.User.id, models.User.name)
            .order_by(desc(models.UserStatistics.best_streak))
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
                (models.User.id).label("user_id"),
                models.User.name,
                models.UserStatistics.current_streak,
            )
            .join(
                models.UserStatistics, models.User.id == models.UserStatistics.user_id
            )
            # .group_by(models.User.id, models.User.name)
            .order_by(desc(models.UserStatistics.current_streak))
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e


def user_ranking_achievements(db: Session, limit: int = None):
    return (
        db.query(
            models.UserAchievement.user_id, func.count(models.UserAchievement.user_id)
        )
        .group_by(models.UserAchievement.user_id)
        .order_by(func.count(models.UserAchievement.user_id).desc())
        .limit(limit)
    )


def user_played_games(db: Session, limit: int = None):
    try:
        stmt = (
            select(
                models.UserGame.user_id,
                func.count(models.UserGame.game_id).label("game_count"),
                models.User.name,
            )
            .join(models.User, models.User.id == models.UserGame.user_id)
            .group_by(models.UserGame.user_id, models.User.name)
            .order_by(func.count(models.UserGame.game_id).desc())
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
                models.UserGame.user_id,
                models.User.name,
                func.count(models.UserGame.game_id),
            )
            .group_by(models.UserGame.user_id)
            .join(models.User, models.User.id == models.UserGame.user_id)
            .filter(models.UserGame.completed == 1)
            .order_by(func.count(models.UserGame.game_id).desc())
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
                models.TimeEntry.project_clockify_id,
                models.Game.name,
                models.TimeEntry.start,
            )
            .join(
                models.Game,
                models.Game.clockify_id == models.TimeEntry.project_clockify_id,
            )
            .order_by(desc(models.TimeEntry.start))
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e


def user_last_played_games(db: Session, limit: int = None):
    try:
        stmt = (
            select(
                models.TimeEntry.project_clockify_id,
                models.TimeEntry.user_id,
                models.TimeEntry.start,
                models.User.name,
            )
            .join(models.User, models.User.id == models.TimeEntry.user_id)
            .filter(models.User.username == 1)
            .order_by(func.count(models.UserGame.game_id).desc())
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e


def games_most_played(db: Session, limit: int = 10):
    try:
        stmt = (
            select(
                (models.Game.id).label("game_id"),
                models.Game.name,
                models.GameStatistics.played_time,
            )
            .join(
                models.GameStatistics, models.Game.id == models.GameStatistics.game_id
            )
            # .group_by(models.User.id, models.User.name)
            .order_by(desc(models.GameStatistics.played_time))
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e

    stmt = (
        select(models.Game.name, models.Game.played_time)
        .order_by(desc(models.Game.played_time))
        .limit(limit)
    )
    result_db = db.execute(stmt).fetchall()
    return result_db


def platform_played_games(db: Session, limit: int = None):
    try:
        stmt = (
            select(
                (models.UserGame.platform).label("tag_id"),
                models.ClockifyTag.name,
                func.count(models.UserGame.platform),
            )
            .join(
                models.ClockifyTag,
                models.UserGame.platform == models.ClockifyTag.id,
            )
            .group_by(models.UserGame.platform)
            .order_by(func.count(models.UserGame.platform).desc())
            .limit(limit)
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e
