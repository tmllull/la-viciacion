import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ...utils import actions
from ...utils import actions as actions
from ...utils import logger
from ...utils import my_utils as utils
from ...utils.clockify_api import ClockifyApi
from .. import models, schemas

clockify = ClockifyApi()


def get_users_played_time(db: Session):
    stmt = select(
        models.TimeEntries.user_id, func.sum(models.TimeEntries.duration)
    ).group_by(models.TimeEntries.user_id)
    return db.execute(stmt)


def get_user_played_time(db: Session, user_id: str) -> list[models.TimeEntries]:
    stmt = (
        select(
            models.TimeEntries.user_id,
            func.sum(models.TimeEntries.duration),
        )
        .where(models.TimeEntries.user_id == user_id)
        .group_by(models.TimeEntries.project)
    )
    return db.execute(stmt)


def get_games_played_time(db: Session):
    stmt = select(
        models.TimeEntries.project, func.sum(models.TimeEntries.duration)
    ).group_by(models.TimeEntries.project)
    result = db.execute(stmt)
    return result


def get_game_played_time(db: Session, game):
    stmt = select(
        models.TimeEntries.project, func.sum(models.TimeEntries.duration)
    ).where(models.TimeEntries.project == game)
    result = db.execute(stmt)
    return result


def get_user_games_played_time(db: Session, user_id: str) -> list[models.TimeEntries]:
    stmt = (
        select(
            models.TimeEntries.project,
            func.sum(models.TimeEntries.duration),
        )
        .where(models.TimeEntries.user_id == user_id)
        .group_by(models.TimeEntries.project)
    )
    return db.execute(stmt)


def get_time_entries(db: Session, date: str = None) -> list[models.TimeEntries]:
    if date is None:
        return db.query(models.TimeEntries).order_by(models.TimeEntries.user_id)
    else:
        return (
            db.query(models.TimeEntries)
            .filter(models.TimeEntries.start >= date)
            .order_by(models.TimeEntries.user_id)
        )
