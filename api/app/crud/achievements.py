import datetime
import json
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..database import models, schemas
from ..utils import actions as actions
from ..utils import logger
from ..utils import my_utils as utils
from ..utils.achievements import AchievementsElems
from ..utils.clockify_api import ClockifyApi

clockify = ClockifyApi()


######################
#### ACHIEVEMENTS ####
######################


def populate_achievements(db: Session):
    logger.info("Populating achievements")
    for achievement in list(AchievementsElems):
        key = achievement.name
        title = achievement.value["title"]
        message = achievement.value["message"]
        ach_db = (
            db.query(models.Achievement).filter(models.Achievement.key == key).first()
        )
        if ach_db is None:
            try:
                achievement = models.Achievement(key=key, title=title, message=message)
                db.add(achievement)
                db.commit()
                # db.refresh(achievement)
            except SQLAlchemyError as e:
                db.rollback()
                logger.info("Error adding achievement: " + str(e))
        else:
            # logger.info("Updating achievement")
            stmt = (
                update(models.Achievement)
                .where(models.Achievement.key == key)
                .values(title=title, message=message)
            )
            db.execute(stmt)
            db.commit()
        # print(achievement, "->", achievement.value)


def get_achievements_list(db: Session):
    return db.query(models.Achievement)


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
