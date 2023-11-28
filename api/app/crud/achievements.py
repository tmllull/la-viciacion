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


######################
#### ACHIEVEMENTS ####
######################


def get_achievements_list(db: Session):
    return db.query(
        models.Achievement.achievement,
    )


def lose_streak(db: Session, player, streak, date=None):
    logger.info("TBI")
    # if streak == 0:
    #     stmt = select(models.User.current_streak).where(models.User.name == player)
    #     last = db.execute(stmt).first()
    #     if last[0] != None and last[0] != 0:
    #         stmt = (
    #             update(models.User)
    #             .where(models.User.name == player)
    #             .values(current_streak=streak)
    #         )
    #         db.execute(stmt)
    #         db.commit()
    #         return last
    # stmt = (
    #     update(models.User)
    #     .where(models.User.name == player)
    #     .values(last_streak=streak)
    # )
    # db.execute(stmt)
    # db.commit()
    return False


def best_streak(db: Session, player, streak, date):
    stmt = select(models.Users.best_streak).where(models.Users.name == player)
    best_streak = db.execute(stmt).first()
    if best_streak is None or best_streak <= streak:
        stmt = (
            update(models.Users)
            .where(models.Users.name == player)
            .values(best_streak=streak, best_streak_date=date)
        )
        db.execute(stmt)
        db.commit()


def current_streak(db: Session, player, streak):
    stmt = (
        update(models.Users)
        .where(models.Users.name == player)
        .values(current_streak=streak)
    )
    db.execute(stmt)
    db.commit()
