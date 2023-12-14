import datetime
import json
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..crud import time_entries as time_entries
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


class Achievements:
    from ..utils.achievements import AchievementsElems

    def __init__(self, silent: bool = False) -> None:
        self.silent = silent

    def populate_achievements(self, db: Session):
        logger.info("Populating achievements")
        for achievement in list(AchievementsElems):
            key = achievement.name
            title = achievement.value["title"]
            message = achievement.value["message"]
            ach_db = (
                db.query(models.Achievement)
                .filter(models.Achievement.key == key)
                .first()
            )
            if ach_db is None:
                try:
                    achievement = models.Achievement(
                        key=key, title=title, message=message
                    )
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

    def get_achievements_list(self, db: Session):
        return db.query(models.Achievement)

    def get_ach_by_key(self, db: Session, key: str):
        return (
            db.query(models.Achievement.id)
            .filter(models.Achievement.key == key)
            .first()
        )

    def check_already_achieved(self, db: Session, user_id: int, key: str):
        ach_id = self.get_ach_by_key(db, str(key))
        already_achieved = (
            db.query(models.UserAchievement)
            .filter(
                models.UserAchievement.user_id == user_id,
                models.UserAchievement.achievement_id == ach_id[0],
            )
            .first()
        )
        if already_achieved is None:
            return False
        return True

    def set_user_achievement(
        self, db: Session, user_id: int, key: str, date: str = None
    ):
        if date is None:
            date = datetime.datetime.now()
        else:
            date = utils.convert_date_from_text(date)
        ach_id = self.get_ach_by_key(db, key)
        user_achievement = models.UserAchievement(
            user_id=user_id, achievement_id=ach_id[0], date=date
        )
        db.add(user_achievement)
        db.commit()
        # return

    ######################
    ##### ACH CHECKS #####
    ######################

    def user_played_total_time(
        self, db: Session, user: models.User, played_time: int, date: str = None
    ):
        logger.info(played_time)
        played_time = played_time / 60 / 60
        logger.info(played_time)
        logger.info("Check played time achievement for " + str(played_time) + " h")
        # 100 h
        if played_time >= 100 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_100_HOURS.name
        ):
            logger.info("Set achievement 100h")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_100_HOURS.name, date
            )

        # 200 h
        if played_time >= 200 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_200_HOURS.name
        ):
            logger.info("Set achievement 200h")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_200_HOURS.name, date
            )

        # 500 h
        if played_time >= 500 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_500_HOURS.name
        ):
            logger.info("Set achievement 500h")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_500_HOURS.name, date
            )

        # 1000 h
        if played_time >= 1000 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_1000_HOURS.name
        ):
            logger.info("Set achievement 1000h")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_1000_HOURS.name, date
            )
        return

    def user_played_day_time(
        self, db: Session, user: models.User, played_time: int, date: str = None
    ):
        # # 5 min
        # if (
        #     played_time > 0
        #     and played_time <= 5
        #     and not self.check_already_achieved(
        #         db, user.id, AchievementsElems.PLAYED_LESS_5_MIN
        #     )
        # ):
        #     pass

        played_time = played_time / 60

        # 4 hours
        if played_time >= 4 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_4_HOURS_DAY
        ):
            pass

        # 8 hours
        if played_time >= 8 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_8_HOURS_DAY
        ):
            pass

        # 12 hour
        if played_time >= 12 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_12_HOURS_DAY
        ):
            pass

        # 16 hours
        if played_time >= 16 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_16_HOURS_DAY
        ):
            pass

        return

    def user_session_time(self, db: Session, user: models.User):
        # -5 min
        if not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_LESS_5_MIN_SESSION.name
        ):
            time_entry = time_entries.get_time_entry_by_time(db, user.id, 5 * 60, 2)
            if time_entry is not None:
                self.set_user_achievement(
                    db,
                    user.id,
                    AchievementsElems.PLAYED_LESS_5_MIN_SESSION.name,
                    str(time_entry.start),
                )

        # +4 hours
        if not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_4_HOURS_SESSION.name
        ):
            time_entry = time_entries.get_time_entry_by_time(
                db, user.id, 4 * 60 * 60, 3
            )
            if time_entry is not None:
                self.set_user_achievement(
                    db,
                    user.id,
                    AchievementsElems.PLAYED_4_HOURS_SESSION.name,
                    str(time_entry.start),
                )

        # +8 hours
        if not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_8_HOURS_SESSION.name
        ):
            time_entry = time_entries.get_time_entry_by_time(
                db, user.id, 8 * 60 * 60, 3
            )
            if time_entry is not None:
                self.set_user_achievement(
                    db,
                    user.id,
                    AchievementsElems.PLAYED_8_HOURS_SESSION.name,
                    str(time_entry.start),
                )

    def user_played_total_days(
        self, db: Session, user: models.User, total_days: int, date: str = None
    ):
        # 7 days

        # 15 days

        # 30 days

        # 60 days

        # 100 days

        # 200 days

        # 300 days

        # 365 days
        return

    def user_played_total_games(
        self, db: Session, user: models.User, played_games: int, date: str = None
    ):
        # 42

        # 100

        return

    def user_played_hours_game(
        self,
        db: Session,
        user: models.User,
        game_id: str,
        played_time: int,
        date: str = None,
    ):
        # 100 h

        # 500 h

        # 1000 h
        return

    def user_streak(
        self, db: Session, user: models.User, streak: int, date: str = None
    ):
        # 7 days

        # 15 days

        # 30 days

        # 60 days

        # 100 days

        # 200 days

        # 300 days

        # 365 days
        return

    def just_in_time(
        self,
        db: Session,
        user: models.User,
        played_time: int,
        avg_time: int,
        game_id: str,
        date: str = None,
    ):
        return

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
