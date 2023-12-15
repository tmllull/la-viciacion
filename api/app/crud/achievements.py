import datetime
import json
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..crud import time_entries, users
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

    def check_already_achieved(
        self, db: Session, user_id: int, key: str, date: str = None
    ):
        if date is not None:
            year = datetime.datetime.strptime(date, "%Y-%m-%d").year
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
        played_time = played_time / 60 / 60
        # To create messages, use the follow example, and adapt to every message
        # user = user.name
        # msg = AchievementsElems.PLAYED_100_HOURS.value["message"].format(name)
        # 100 h
        logger.info("Check total played time achievements")
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
        logger.info("Check session time achievements...")
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

    def user_played_total_days(self, db: Session, user: models.User, total_days: int):
        # 7 days
        if total_days >= 7 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_7_DAYS.name
        ):
            self.set_user_achievement(db, user.id, AchievementsElems.PLAYED_7_DAYS.name)
        # 15 days
        if total_days >= 15 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_15_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_15_DAYS.name
            )
        # 30 days
        if total_days >= 30 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_30_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_30_DAYS.name
            )
        # 60 days
        if total_days >= 60 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_60_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_60_DAYS.name
            )
        # 100 days
        if total_days >= 100 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_100_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_100_DAYS.name
            )
        # 200 days
        if total_days >= 200 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_200_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_200_DAYS.name
            )
        # 300 days
        if total_days >= 300 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_300_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_300_DAYS.name
            )
        # 365 days
        if total_days >= 365 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_365_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_365_DAYS.name
            )

    def user_played_total_games(self, db: Session, user: models.User, date: str = None):
        logger.info("Check total played games achievements...")
        played_games = users.get_games(db, user.id)
        # 10
        # logger.info("Played games for " + user.name + ": " + str(len(played_games)))
        if len(played_games) >= 10 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_10_GAMES.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_10_GAMES.name
            )
        # 42
        if len(played_games) >= 42 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_42_GAMES.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_42_GAMES.name
            )
        # 50
        if len(played_games) >= 50 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_50_GAMES.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_50_GAMES.name
            )
        # 100
        if len(played_games) >= 100 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_100_GAMES.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_100_GAMES.name
            )

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
        self,
        db: Session,
        user: models.User,
        streak: int,
        date: datetime.datetime = None,
    ):
        logger.info("Checking streaks achievements")
        if date is not None:
            date = date.strftime("%Y-%m-%d %H:%M:%S")
        # 7 days
        if streak >= 7 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_7_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_7_DAYS.name, date
            )
        # 15 days
        if streak >= 15 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_15_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_15_DAYS.name, date
            )
        # 30 days
        if streak >= 30 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_30_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_30_DAYS.name, date
            )
        # 60 days
        if streak >= 60 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_60_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_60_DAYS.name, date
            )
        # 100 days
        if streak >= 100 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_100_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_100_DAYS.name, date
            )
        # 200 days
        if streak >= 200 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_200_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_200_DAYS.name, date
            )
        # 300 days
        if streak >= 300 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_300_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_300_DAYS.name, date
            )
        # 365 days
        if streak >= 365 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_365_DAYS.name
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_365_DAYS.name, date
            )
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
