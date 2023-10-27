import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ...database.crud import users
from ...utils import actions as actions
from ...utils import logger
from ...utils import my_utils as utils
from ...utils.clockify_api import ClockifyApi
from .. import models, schemas

clockify = ClockifyApi()


######################
#### ACHIEVEMENTS ####
######################


def get_achievements_list(db: Session):
    return db.query(
        models.Achievement.achievement,
    )


def lose_streak(db: Session, player, streak, date=None):
    if streak == 0:
        stmt = select(models.User.last_streak).where(models.User.name == player)
        last = db.execute(stmt).first()
        if last[0] != None and last[0] != 0:
            stmt = (
                update(models.User)
                .where(models.User.name == player)
                .values(last_streak=streak, last_streak_date=date)
            )
            db.execute(stmt)
            db.commit()
            return last
    stmt = (
        update(models.User)
        .where(models.User.name == player)
        .values(last_streak=streak, last_streak_date=date)
    )
    db.execute(stmt)
    db.commit()
    return False


def best_streak(db: Session, player, streak, date):
    stmt = select(models.User.best_streak).where(models.User.name == player)
    best_streak = db.execute(stmt).first()
    if best_streak is None or best_streak <= streak:
        stmt = (
            update(models.User)
            .where(models.User.name == player)
            .values(best_streak=streak, best_streak_date=date)
        )
        db.execute(stmt)
        db.commit()


def current_streak(db: Session, player, streak):
    stmt = (
        update(models.User)
        .where(models.User.name == player)
        .values(current_streak=streak)
    )
    db.execute(stmt)
    db.commit()


####################
##### Clockify #####
####################


# def sync_clockify_entries(db: Session, user_id, entries):
#     user = users.get_user(db, user=user_id)
#     logger.info("Sync entries for user " + str(user.name))
#     for entry in entries:
#         try:
#             start = entry["timeInterval"]["start"]
#             end = entry["timeInterval"]["end"]
#             duration = entry["timeInterval"]["duration"]
#             if end is None:
#                 end = ""
#             if duration is None:
#                 duration = ""
#             start = utils.change_timezone_clockify(start)
#             if end != "":
#                 end = utils.change_timezone_clockify(end)
#             project_name = clockify.get_project(entry["projectId"])["name"]
#             stmt = select(models.TimeEntries).where(
#                 models.TimeEntries.id == entry["id"]
#             )
#             exists = db.execute(stmt).first()
#             if not exists:
#                 new_entry = models.TimeEntries(
#                     id=entry["id"],
#                     user=user.name,
#                     user_id=user.id,
#                     user_clockify_id=user.clockify_id,
#                     project=project_name,
#                     project_id=entry["projectId"],
#                     start=start,
#                     end=end,
#                     duration=actions.convert_clockify_duration(duration),
#                 )
#                 db.add(new_entry)
#             else:
#                 stmt = (
#                     update(models.TimeEntries)
#                     .where(models.TimeEntries.id == entry["id"])
#                     .values(
#                         user=user.name,
#                         project=project_name,
#                         project_id=entry["projectId"],
#                         start=start,
#                         end=end,
#                         duration=actions.convert_clockify_duration(duration),
#                     )
#                 )
#                 db.execute(stmt)
#             db.commit()
#         except Exception as e:
#             db.rollback()
#             logger.info("Error adding new entry " + str(entry) + ": " + str(e))
#             raise e
#         # logger.info(entry["id"])
#         # exit()
#     return


# def get_time_entries(db: Session, date: str = None) -> list[models.TimeEntries]:
#     if date is None:
#         return db.query(models.TimeEntries).order_by(models.TimeEntries.user_id)
#     else:
#         return (
#             db.query(models.TimeEntries)
#             .filter(models.TimeEntries.start >= date)
#             .order_by(models.TimeEntries.user_id)
#         )


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
