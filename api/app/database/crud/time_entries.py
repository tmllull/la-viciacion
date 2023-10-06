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
from . import games, users

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


def get_time_entries(db: Session, start_date: str = None) -> list[models.TimeEntries]:
    if start_date is None:
        return db.query(models.TimeEntries).order_by(models.TimeEntries.user_id)
    else:
        logger.info(start_date)
        return (
            db.query(models.TimeEntries)
            .filter(models.TimeEntries.start >= start_date)
            .order_by(models.TimeEntries.user_id)
        )


def get_played_days(db: Session, user_id: int) -> list[models.TimeEntries]:
    played_days = []
    played_start_days = (
        db.query(models.TimeEntries.start_date)
        .filter(models.TimeEntries.user_id == user_id)
        .group_by(models.TimeEntries.start_date)
    )
    for played_day in played_start_days:
        played_days.append(played_day[0])
    played_end_days = (
        db.query(models.TimeEntries.end_date)
        .filter(models.TimeEntries.user_id == user_id)
        .group_by(models.TimeEntries.end_date)
    )
    for played_day in played_end_days:
        if (
            played_day[0] != ""
            and played_day[0] is not None
            and played_day[0] not in played_days
        ):
            played_days.append(played_day[0])
    return played_days
    # return played_start_days.count()
    # return (
    #     db.query(models.TimeEntries.start_date)
    #     .filter(models.TimeEntries.user_id == user_id)
    #     .group_by(models.TimeEntries.start_date)
    #     .count()
    # )


def sync_clockify_entries_db(db: Session, user: models.User, entries):
    logger.info("Sync " + str(len(entries)) + " entries for user " + str(user.name))
    for entry in entries:
        try:
            start = entry["timeInterval"]["start"]
            end = entry["timeInterval"]["end"]
            duration = entry["timeInterval"]["duration"]
            start_date = ""
            end_date = ""
            if end is None:
                end = ""
            if duration is None:
                duration = ""
            start = utils.change_timezone_clockify(start)
            start_date = utils.date_from_datetime(start)
            if end != "":
                end = utils.change_timezone_clockify(end)
                end_date = utils.date_from_datetime(end)
            # project_name = clockify_api.get_project(entry["projectId"])["name"]
            project = games.get_game_by_clockify_id(db, entry["projectId"])
            project_name = project.name
            stmt = select(models.TimeEntries).where(
                models.TimeEntries.id == entry["id"]
            )
            exists = db.execute(stmt).first()
            if not exists:
                new_entry = models.TimeEntries(
                    id=entry["id"],
                    user=user.name,
                    user_id=user.id,
                    user_clockify_id=user.clockify_id,
                    project=project_name,
                    project_id=entry["projectId"],
                    start=start,
                    start_date=start_date,
                    end=end,
                    end_date=end_date,
                    duration=utils.convert_clockify_duration(duration),
                )
                db.add(new_entry)
            else:
                stmt = (
                    update(models.TimeEntries)
                    .where(models.TimeEntries.id == entry["id"])
                    .values(
                        user=user.name,
                        project=project_name,
                        project_id=entry["projectId"],
                        start=start,
                        start_date=start_date,
                        end=end,
                        end_date=end_date,
                        duration=utils.convert_clockify_duration(duration),
                    )
                )
                db.execute(stmt)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.info("Error adding new entry " + str(entry) + ": " + str(e))
            raise e
        # logger.info(entry["id"])
        # exit()
    return
