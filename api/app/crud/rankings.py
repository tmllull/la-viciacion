import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ..database import models, schemas
from ..utils import actions as actions
from ..utils import logger
from ..utils import my_utils as utils
from ..utils.clockify_api import ClockifyApi

clockify = ClockifyApi()

####################
##### RANKINGS #####
####################


def hours_players(db: Session) -> list[models.Users]:
    try:
        return db.query(models.Users.name, models.Users.played_time).order_by(
            desc(models.Users.played_time)
        )
    except Exception as e:
        logger.info(e)


def days_players(db: Session) -> list[models.Users]:
    try:
        return db.query(models.Users.name, models.Users.played_days).order_by(
            desc(models.Users.played_days)
        )
    except Exception as e:
        logger.info(e)
        raise e


def best_streak(db: Session):
    try:
        return db.query(models.Users.name, models.Users.best_streak).order_by(
            desc(models.Users.best_streak)
        )
    except Exception as e:
        logger.info(e)
        raise e


def current_streak(db: Session):
    try:
        return db.query(models.Users.name, models.Users.current_streak).order_by(
            desc(models.Users.current_streak)
        )
    except Exception as e:
        logger.info(e)
        raise e


def ranking_achievements(db: Session):
    return (
        db.query(
            models.UserAchievements.user_id, func.count(models.UserAchievements.user_id)
        )
        .group_by(models.UserAchievements.user_id)
        .order_by(func.count(models.UserAchievements.user_id).desc())
        .all()
    )


def user_played_games(db: Session):
    result = (
        db.query(models.UsersGames.user_id, func.count(models.UsersGames.game_id))
        .group_by(models.UsersGames.user_id)
        .order_by(func.count(models.UsersGames.game_id).desc())
        .all()
    )
    return result


def ranking_completed_games(db: Session):
    return (
        db.query(models.UsersGames.user_id, func.count(models.UsersGames.game_id))
        .group_by(models.UsersGames.user_id)
        .filter_by(completed=1)
        .order_by(func.count(models.UsersGames.game_id).desc())
        .all()
    )


def ranking_last_played_games(db: Session):
    stmt = select(
        models.TimeEntries.project_clockify_id,
        models.TimeEntries.user,
        models.TimeEntries.start,
    ).order_by(desc(models.TimeEntries.start))
    return db.execute(stmt).fetchall()


def most_played_games(db: Session, limit: int = 10):
    stmt = (
        select(models.GamesInfo.name, models.GamesInfo.played_time)
        .order_by(desc(models.GamesInfo.played_time))
        .limit(limit)
    )
    return db.execute(stmt).fetchall()
