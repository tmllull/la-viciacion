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

clockify_api = ClockifyApi()


def get_users_played_time(db: Session):
    stmt = select(
        models.TimeEntries.user_id, func.sum(models.TimeEntries.duration)
    ).group_by(models.TimeEntries.user_id)
    return db.execute(stmt)


def get_user_played_time(db: Session, user_id: str):
    stmt = (
        select(
            models.TimeEntries.user_id,
            func.sum(models.TimeEntries.duration),
        )
        .where(models.TimeEntries.user_id == user_id)
        .group_by(models.TimeEntries.user_id)
    )
    return db.execute(stmt).first()


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


def get_played_days(db: Session, user_id: int) -> list:
    played_days = []
    # query = db.query(func.DATE(models.TimeEntries.start)).distinct().count()
    played_start_days = (
        db.query(func.DATE(models.TimeEntries.start))
        .filter(models.TimeEntries.user_id == user_id)
        .distinct()
    )
    for played_day in played_start_days:
        played_days.append(played_day[0])
    # logger.info(played_days)
    played_end_days = (
        db.query(func.DATE(models.TimeEntries.end))
        .filter(models.TimeEntries.user_id == user_id)
        .distinct()
    )
    for played_day in played_end_days:
        if (
            played_day[0] != ""
            and played_day[0] is not None
            and played_day[0] not in played_days
        ):
            played_days.append(played_day[0])
    return sorted(played_days)


async def sync_clockify_entries_db(db: Session, user: models.User, entries):
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
            # start_date = utils.date_from_datetime(start)
            if end != "":
                end = utils.change_timezone_clockify(end)
                # end_date = utils.date_from_datetime(end)
            # project_name = clockify_api.get_project(entry["projectId"])["name"]
            project = games.get_game_by_clockify_id(db, entry["projectId"])
            if project is not None:
                project_name = project.name
            else:
                project = clockify_api.get_project(entry["projectId"])
                project_name = project["name"]
                new_game = await utils.get_new_game_info(project)
                games.new_game(db, new_game)
            already_playing = users.get_game(db, user.id, project_name)
            if not already_playing:
                new_user_game = schemas.NewGameUser(game=project_name, platform="TBD")
                users.add_new_game(db, new_user_game, user)
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
                    # start_date=start_date,
                    end=end,
                    # end_date=end_date,
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
                        # start_date=start_date,
                        end=end,
                        # end_date=end_date,
                        duration=utils.convert_clockify_duration(duration),
                    )
                )
                db.execute(stmt)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.info("Error adding entry " + str(entry) + ": " + str(e))
            raise e
        # logger.info(entry["id"])
        # exit()
    return


def get_all_played_games(db: Session):
    stmt = select(models.TimeEntries.project, models.TimeEntries.project_id)
    return db.execute(stmt)
