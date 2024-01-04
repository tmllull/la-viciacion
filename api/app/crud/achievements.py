import datetime
import json
from typing import List, Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..config import Config
from ..crud import time_entries, users
from ..database import models, schemas
from ..utils import actions as actions
from ..utils import logger
from ..utils import my_utils as utils
from ..utils.achievements import AchievementsElems
from ..utils.clockify_api import ClockifyApi

clockify = ClockifyApi()
config = Config()

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
        self, db: Session, user_id: int, key: str, game_id: str = None, date: str = None
    ):
        if date is None:
            date = datetime.datetime.now()
        else:
            date = utils.convert_date_from_text(date)
        ach_id = self.get_ach_by_key(db, key)
        user_achievement = models.UserAchievement(
            user_id=user_id, achievement_id=ach_id[0], date=date, game_id=game_id
        )
        db.add(user_achievement)
        db.commit()
        # return

    ######################
    ##### ACH CHECKS #####
    ######################

    async def user_played_total_time(
        self,
        db: Session,
        user: models.User,
        played_time: int,
        date: str = None,
        silent: bool = False,
    ):
        logger.info("Check total played time achievements...")
        if played_time is None:
            return
        played_time = played_time / 60 / 60
        # To create messages, use the follow example, and adapt to every message
        # user = user.name
        # msg = AchievementsElems.PLAYED_100_HOURS.value["message"].format(name)
        # 100 h
        # logger.info("Check total played time achievements")
        if played_time >= 100 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_100_HOURS.name
        ):
            logger.info("Set achievement 100h")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_100_HOURS.name, date
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_100_HOURS, user=user.name
            )
            await utils.send_message(msg, silent)

        # 200 h
        if played_time >= 200 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_200_HOURS.name
        ):
            logger.info("Set achievement 200h")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_200_HOURS.name, date
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_200_HOURS, user=user.name
            )
            await utils.send_message(msg, silent)

        # 500 h
        if played_time >= 500 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_500_HOURS.name
        ):
            logger.info("Set achievement 500h")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_500_HOURS.name, date
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_500_HOURS, user=user.name
            )
            await utils.send_message(msg, silent)

        # 1000 h
        if played_time >= 1000 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_1000_HOURS.name
        ):
            logger.info("Set achievement 1000h")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_1000_HOURS.name, date
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_1000_HOURS, user=user.name
            )
            await utils.send_message(msg, silent)

    async def user_played_day_time(
        self,
        db: Session,
        user: models.User,
        silent: bool = False,
    ):
        logger.info("Check played time in one day achievements...")
        # played_time = played_time / 60 / 60
        played_days = time_entries.get_played_time_by_day(db, user.id)
        for played_day in played_days:
            date = str(played_day[0])
            if played_day[1] is None:
                continue
            played_time = played_day[1] / 60 / 60
            # 4 hours
            if played_time >= 4 and not self.check_already_achieved(
                db, user.id, AchievementsElems.PLAYED_4_HOURS_DAY.name
            ):
                logger.info("Set achievement 4 hours day")
                self.set_user_achievement(
                    db, user.id, AchievementsElems.PLAYED_4_HOURS_DAY.name, date=date
                )
                msg = utils.get_ach_message(
                    AchievementsElems.PLAYED_4_HOURS_DAY, user=user.name
                )
                await utils.send_message(msg, silent)

            # 8 hours
            if played_time >= 8 and not self.check_already_achieved(
                db, user.id, AchievementsElems.PLAYED_8_HOURS_DAY.name
            ):
                logger.info("Set achievement 8 hours day")
                self.set_user_achievement(
                    db, user.id, AchievementsElems.PLAYED_8_HOURS_DAY.name, date=date
                )
                msg = utils.get_ach_message(
                    AchievementsElems.PLAYED_8_HOURS_DAY, user=user.name
                )
                await utils.send_message(msg, silent)

            # 12 hour
            if played_time >= 12 and not self.check_already_achieved(
                db, user.id, AchievementsElems.PLAYED_12_HOURS_DAY.name
            ):
                logger.info("Set achievement 12 hours day")
                self.set_user_achievement(
                    db, user.id, AchievementsElems.PLAYED_12_HOURS_DAY.name, date=date
                )
                msg = utils.get_ach_message(
                    AchievementsElems.PLAYED_12_HOURS_DAY, user=user.name
                )
                await utils.send_message(msg, silent)

            # 16 hours
            if played_time >= 16 and not self.check_already_achieved(
                db, user.id, AchievementsElems.PLAYED_16_HOURS_DAY.name
            ):
                logger.info("Set achievement 16 hours day")
                self.set_user_achievement(
                    db, user.id, AchievementsElems.PLAYED_16_HOURS_DAY.name, date=date
                )
                msg = utils.get_ach_message(
                    AchievementsElems.PLAYED_16_HOURS_DAY, user=user.name
                )
                await utils.send_message(msg, silent)

    async def user_session_time(
        self, db: Session, user: models.User, silent: bool = False
    ):
        logger.info("Check session played time achievements...")
        # -5 min
        if not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_LESS_5_MIN_SESSION.name
        ):
            time_entry = time_entries.get_time_entry_by_time(db, user.id, 5 * 60, 2)
            if time_entry is not None and time_entry.duration > 0:
                logger.info("Set achievement less 5 minutes session")
                self.set_user_achievement(
                    db,
                    user.id,
                    AchievementsElems.PLAYED_LESS_5_MIN_SESSION.name,
                    game_id=time_entry.project_clockify_id,
                    date=str(time_entry.start),
                )
                msg = utils.get_ach_message(
                    AchievementsElems.PLAYED_LESS_5_MIN_SESSION,
                    user=user.name,
                    db=db,
                    game_id=time_entry.project_clockify_id,
                )
                await utils.send_message(msg, silent)

        # +4 hours
        if not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_4_HOURS_SESSION.name
        ):
            time_entry = time_entries.get_time_entry_by_time(
                db, user.id, 4 * 60 * 60, 3
            )
            if time_entry is not None:
                logger.info("Set achievement 4 hours session")
                self.set_user_achievement(
                    db,
                    user.id,
                    AchievementsElems.PLAYED_4_HOURS_SESSION.name,
                    date=str(time_entry.start),
                )
                msg = utils.get_ach_message(
                    AchievementsElems.PLAYED_4_HOURS_SESSION, user=user.name
                )
                await utils.send_message(msg, silent)

        # +8 hours
        if not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_8_HOURS_SESSION.name
        ):
            time_entry = time_entries.get_time_entry_by_time(
                db, user.id, 8 * 60 * 60, 3
            )
            if time_entry is not None:
                logger.info("Set achievement 8 hours session")
                self.set_user_achievement(
                    db,
                    user.id,
                    AchievementsElems.PLAYED_8_HOURS_SESSION.name,
                    date=str(time_entry.start),
                )
                msg = utils.get_ach_message(
                    AchievementsElems.PLAYED_8_HOURS_SESSION, user=user.name
                )
                await utils.send_message(msg, silent)

    async def user_played_total_days(
        self, db: Session, user: models.User, total_days: list, silent: bool = False
    ):
        logger.info(
            "Check total played days achievements (" + str(len(total_days)) + ")..."
        )
        # achieved_date = total_days[1]
        # 7 days
        if len(total_days) >= 7 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_7_DAYS.name
        ):
            logger.info("Set achievement played 7 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_7_DAYS.name, date=total_days[6]
            )
            msg = utils.get_ach_message(AchievementsElems.PLAYED_7_DAYS, user=user.name)
            await utils.send_message(msg, silent)
        # 15 days
        if len(total_days) >= 15 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_15_DAYS.name
        ):
            logger.info("Set achievement played 15 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_15_DAYS.name, date=total_days[14]
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_15_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)
        # 30 days
        if len(total_days) >= 30 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_30_DAYS.name
        ):
            logger.info("Set achievement played 30 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_30_DAYS.name, date=total_days[29]
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_30_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)
        # 60 days
        if len(total_days) >= 60 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_60_DAYS.name
        ):
            logger.info("Set achievement played 60 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_60_DAYS.name, date=total_days[59]
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_60_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)
        # 100 days
        if len(total_days) >= 100 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_100_DAYS.name
        ):
            logger.info("Set achievement played 100 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_100_DAYS.name, date=total_days[99]
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_100_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)
        # 200 days
        if len(total_days) >= 200 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_200_DAYS.name
        ):
            logger.info("Set achievement played 200 days")
            self.set_user_achievement(
                db,
                user.id,
                AchievementsElems.PLAYED_200_DAYS.name,
                date=total_days[199],
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_200_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)
        # 300 days
        if len(total_days) >= 300 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_300_DAYS.name
        ):
            logger.info("Set achievement played 300 days")
            self.set_user_achievement(
                db,
                user.id,
                AchievementsElems.PLAYED_300_DAYS.name,
                date=total_days[299],
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_300_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)
        # 365 days
        if len(total_days) >= 365 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_365_DAYS.name
        ):
            logger.info("Set achievement played 365 days")
            self.set_user_achievement(
                db,
                user.id,
                AchievementsElems.PLAYED_365_DAYS.name,
                date=total_days[364],
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_365_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)

    async def user_played_total_games(
        self, db: Session, user: models.User, date: str = None, silent: bool = False
    ):
        logger.info("Check total played games achievements...")
        played_games = users.get_games(db, user.id)
        # 10
        # logger.info("Played games for " + user.name + ": " + str(len(played_games)))
        if len(played_games) >= 10 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_10_GAMES.name
        ):
            logger.info("Set achievement played 10 games")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_10_GAMES.name
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_10_GAMES, user=user.name
            )
            await utils.send_message(msg, silent)
        # 42
        if len(played_games) >= 42 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_42_GAMES.name
        ):
            logger.info("Set achievement played 42 games")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_42_GAMES.name
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_42_GAMES, user=user.name
            )
            await utils.send_message(msg, silent)
        # 50
        if len(played_games) >= 50 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_50_GAMES.name
        ):
            logger.info("Set achievement played 50 games")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_50_GAMES.name
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_50_GAMES, user=user.name
            )
            await utils.send_message(msg, silent)
        # 100
        if len(played_games) >= 100 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_100_GAMES.name
        ):
            logger.info("Set achievement played 100 games")
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_100_GAMES.name
            )
            msg = utils.get_ach_message(
                AchievementsElems.PLAYED_100_GAMES, user=user.name
            )
            await utils.send_message(msg, silent)

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

    async def happy_new_year(
        self,
        db: Session,
        user: models.User,
        silent: bool = False,
    ):
        current_season = str(config.CURRENT_SEASON)
        new_year = current_season + "-01-01"
        time_entry = time_entries.get_time_entry_by_date(db, user.id, new_year, 1)
        if time_entry.count() > 0 and not self.check_already_achieved(
            db, user.id, AchievementsElems.HAPPY_NEW_YEAR.name
        ):
            logger.info("Set achievement happy new year")
            self.set_user_achievement(
                db,
                user.id,
                AchievementsElems.HAPPY_NEW_YEAR.name,
                date=str(time_entry[0].start),
            )
            msg = utils.get_ach_message(
                AchievementsElems.HAPPY_NEW_YEAR, user=user.name
            )
            await utils.send_message(msg, silent)

    async def user_streak(
        self,
        db: Session,
        user: models.User,
        streak: int,
        date: datetime.datetime = None,
        silent: bool = False,
    ):
        logger.info("Check streaks achievements...")
        if date is not None:
            date = date.strftime("%Y-%m-%d %H:%M:%S")
        # 7 days
        if streak >= 7 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_7_DAYS.name
        ):
            logger.info("Set achievement streak 7 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_7_DAYS.name, date=date
            )
            msg = utils.get_ach_message(AchievementsElems.STREAK_7_DAYS, user=user.name)
            await utils.send_message(msg, silent)
        # 15 days
        if streak >= 15 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_15_DAYS.name
        ):
            logger.info("Set achievement streak 15 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_15_DAYS.name, date=date
            )
            msg = utils.get_ach_message(
                AchievementsElems.STREAK_15_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)
        # 30 days
        if streak >= 30 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_30_DAYS.name
        ):
            logger.info("Set achievement streak 30 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_30_DAYS.name, date=date
            )
            msg = utils.get_ach_message(
                AchievementsElems.STREAK_30_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)
        # 60 days
        if streak >= 60 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_60_DAYS.name
        ):
            logger.info("Set achievement streak 60 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_60_DAYS.name, date=date
            )
            msg = utils.get_ach_message(
                AchievementsElems.STREAK_60_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)
        # 100 days
        if streak >= 100 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_100_DAYS.name
        ):
            logger.info("Set achievement streak 100 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_100_DAYS.name, date=date
            )
            msg = utils.get_ach_message(
                AchievementsElems.STREAK_100_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)
        # 200 days
        if streak >= 200 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_200_DAYS.name
        ):
            logger.info("Set achievement streak 200 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_200_DAYS.name, date=date
            )
            msg = utils.get_ach_message(
                AchievementsElems.STREAK_200_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)
        # 300 days
        if streak >= 300 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_300_DAYS.name
        ):
            logger.info("Set achievement streak 300 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_300_DAYS.name, date=date
            )
            msg = utils.get_ach_message(
                AchievementsElems.STREAK_300_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)
        # 365 days
        if streak >= 365 and not self.check_already_achieved(
            db, user.id, AchievementsElems.STREAK_365_DAYS.name
        ):
            logger.info("Set achievement streak 365 days")
            self.set_user_achievement(
                db, user.id, AchievementsElems.STREAK_365_DAYS.name, date=date
            )
            msg = utils.get_ach_message(
                AchievementsElems.STREAK_365_DAYS, user=user.name
            )
            await utils.send_message(msg, silent)

    async def teamwork(self, db: Session, silent: bool):
        logger.info("Checking teamwork achievement...")
        user_list = users.get_users(db)
        playing: List[models.User] = []
        for user in user_list:
            has_active_time_entry = time_entries.get_active_time_entry_by_user(db, user)
            if has_active_time_entry is not None:
                playing.append(user)
        logger.info(
            "Playing users: " + str(len(playing)) + "/" + str(user_list.count())
        )
        if len(playing) >= 4:  # and notification_sent is None:
            logger.info("4 or more users are playing!")
            someone_not_achieved = False
            players = ""
            for player in playing:
                players += player.name + ", "
                if not self.check_already_achieved(
                    db, player.id, AchievementsElems.TEAMWORK.name
                ):
                    someone_not_achieved = True
                    logger.info("Set 'Teamwork' achievement for " + player.name)
                    self.set_user_achievement(
                        db, player.id, AchievementsElems.TEAMWORK.name
                    )
            if someone_not_achieved:
                players = players[:-2]
                players = players.rsplit(",", 1)
                players = " y".join(players)
                # TODO: send notification
                msg = utils.get_ach_message(AchievementsElems.TEAMWORK, user=players)
                await utils.send_message(msg, silent)
                # else:
                #     db.delete(notification_all_sent)
            else:
                logger.info("All users unlocked this achievement")

    async def early_riser(self, db: Session, user: models.User, silent: bool):
        logger.info("Checking early riser achievement...")
        entries = time_entries.get_time_entry_by_start_time(db, user.id, hour=5, mode=2)
        if len(entries) > 0 and not self.check_already_achieved(
            db, user.id, AchievementsElems.EARLY_RISER.name
        ):
            logger.info("Set achievement early riser")
            self.set_user_achievement(
                db,
                user.id,
                AchievementsElems.EARLY_RISER.name,
                str(date=entries[0].start),
            )
            msg = utils.get_ach_message(AchievementsElems.EARLY_RISER, user=user.name)
            await utils.send_message(msg, silent)
        # for entry in entries:
        #     logger.info(entry.start)

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
