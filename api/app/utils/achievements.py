import datetime
from enum import Enum

from sqlalchemy import update
from sqlalchemy.orm import Session

from ..database import models
from . import my_utils as utils


class AchievementsElems(Enum):
    # Format -> KEY = {"title":"", "message":""}
    # Time day
    PLAYED_LESS_5_MIN = {"title": "Lo he abierto sin querer", "message": "###"}
    PLAYED_4_HOURS_DAY = {
        "title": "Una jornada laboral",
        "message": "El otro mensaje",
    }
    PLAYED_8_HOURS_DAY = {
        "title": "Una jornada laboral",
        "message": "El otro mensaje",
    }
    PLAYED_12_HOURS_DAY = {
        "title": "Media jornada, 12 horas",
        "message": "El otro mensaje",
    }
    PLAYED_16_HOURS_DAY = {
        "title": "No paro ni a cagar",
        "message": "El otro mensaje",
    }

    # Time on game
    PLAYED_8_HOURS_GAME_DAY = {
        "title": "Mi trabajo es jugar",
        "message": "Lo de estar 8 horas trabajando no suele gustar, pero jugando ya es otra cosa. "
        + ""
        + "USER"
        + " acaba de jugar 8 horas (o más) a _"
        + "GAME"
        + "_ en un mismo día; cualquira diría que le está gustando.",
    }
    PLAYED_8_HOURS_GAME_DAY_ONE_SESSION = {
        "title": "Mi trabajo es jugar (sin parar)",
        "message": "Lo de estar 8 horas trabajando no suele gustar, pero jugando ya es otra cosa. "
        + ""
        + "USER"
        + " acaba de cascarse 8 horas seguidas (o más) jugando a _"
        + "GAME"
        + "_; cualquira diría que le está gustando.",
    }
    PLAYED_100_HOURS_GAME = {
        "title": "Una jornada laboral",
        "message": "El otro mensaje",
    }

    # Total time
    PLAYED_100_HOURS = {"title": "", "message": ""}
    PLAYED_200_HOURS = {"title": "", "message": ""}
    PLAYED_500_HOURS = {"title": "", "message": ""}
    PLAYED_1000_HOURS = {"title": "", "message": ""}

    # Games
    PLAYED_42_GAMES = {
        "title": "La respuesta",
        "message": "USER ha jugado a la mágica cifra de 42 juegos."
        + " No sabemos si tendrá la respuesta al sentido de la vida, "
        + "al universo y todo lo demás, pero lo que seguro que tiene "
        + "es mucho tiempo libre.",
    }
    PLAYED_100_GAMES = {
        "title": "100 juegos (jugados)",
        "message": "A 100 juegos acaba de jugar "
        + "USER. Estamos hablando de arrancar un nuevo"
        + " juego cada 3,65 días (si dejara de empezar juegos). Pensemos en ello.",
    }
    COMPLETED_42_GAMES = {
        "title": "La respuesta (de verdad)",
        "message": "Si empezar 42 juegos ya es todo un logro, no hablemos de acabar 42. "
        + "Ha quedado patente que a "
        + "USER"
        + " la vida más allá de la puerta de casa no le importa lo más mínimo.",
    }
    COMPLETED_100_GAMES = {"title": "100 games", "message": ""}
    PLAYED_5_GAMES_DAY = {"title": "", "message": ""}
    PLAYED_10_GAMES_DAY = {"title": "", "message": ""}

    # Total days
    PLAYED_7_DAYS = {"title": "", "message": ""}
    PLAYED_15_DAYS = {"title": "", "message": ""}
    PLAYED_30_DAYS = {"title": "", "message": ""}
    PLAYED_60_DAYS = {"title": "", "message": ""}
    PLAYED_100_DAYS = {"title": "", "message": ""}
    PLAYED_200_DAYS = {"title": "", "message": ""}
    PLAYED_300_DAYS = {"title": "", "message": ""}
    PLAYED_365_DAYS = {"title": "", "message": ""}

    # Streaks
    STREAK_7_DAYS = {"title": "", "message": ""}
    STREAK_15_DAYS = {"title": "", "message": ""}
    STREAK_30_DAYS = {"title": "", "message": ""}
    STREAK_60_DAYS = {"title": "", "message": ""}
    STREAK_100_DAYS = {"title": "", "message": ""}
    STREAK_200_DAYS = {"title": "", "message": ""}
    STREAK_300_DAYS = {"title": "", "message": ""}
    STREAK_365_DAYS = {"title": "", "message": ""}

    # Others
    JUST_IN_TIME = {"title": "Justo a tiempo", "message": ""}


class Achievements:
    from .achievements import AchievementsElems

    def __init__(self, silent: bool = False) -> None:
        self.silent = silent

    def get_ach_by_key(self, db: Session, key: str):
        return (
            db.query(models.Achievement.id)
            .filter(models.Achievement.key == key)
            .first()
        )

    def check_already_achieved(self, db: Session, user_id: int, key: str):
        ach_id = self.get_ach_by_key(db, key)
        already_achieved = (
            db.query(models.UserAchievement)
            .filter(
                models.UserAchievement.user_id == user_id,
                models.UserAchievement.achievement_id == ach_id,
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
            user_id=user_id, achievement_id=ach_id, date=date
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
        played_time = played_time / 60
        # 100 h
        if played_time >= 100 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_100_HOURS
        ):
            self.set_user_achievement(
                db, user.id, AchievementsElems.PLAYED_100_HOURS, date
            )
        return
        # 200 h
        if played_time >= 200 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_200_HOURS
        ):
            pass

        # 500 h
        if played_time >= 500 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_500_HOURS
        ):
            pass

        # 1000 h
        if played_time >= 1000 and not self.check_already_achieved(
            db, user.id, AchievementsElems.PLAYED_1000_HOURS
        ):
            pass
        return

    def user_played_day_time(
        self, db: Session, user: models.User, played_time: int, date: str = None
    ):
        # 5 min
        if (
            played_time > 0
            and played_time <= 5
            and not self.check_already_achieved(
                db, user.id, AchievementsElems.PLAYED_LESS_5_MIN
            )
        ):
            pass

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

    def user_session_time(
        self, db: Session, user: models.User, played_time: int, date: str = None
    ):
        # 5 min

        # 4 hours

        # 8 hours

        return

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
