import datetime
from enum import Enum
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.exc import SQLAlchemyError
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


class Achievements(str, Enum):
    # Format -> KEY = {"title":"", "message":""}
    # Time
    PLAYED_LESS_5_MIN = {"title": "*Lo he abierto sin querer*", "message": "###"}
    PLAYED_8_HOURS_DAY = {
        "title": "*Una jornada laboral*",
        "message": "El otro mensaje",
    }
    PLAYED_12_HOURS_DAY = {
        "title": "*Media jornada, 12 horas*",
        "message": "El otro mensaje",
    }
    PLAYED_16_HOURS_DAY = {
        "title": "*No paro ni a cagar*",
        "message": "El otro mensaje",
    }
    PLAYED_8_HOURS_GAME_DAY = {
        "title": "*Mi trabajo es jugar*",
        "message": "Lo de estar 8 horas trabajando no suele gustar, pero jugando ya es otra cosa. "
        + "*"
        + "USER"
        + "* acaba de jugar 8 horas (o más) a _"
        + "GAME"
        + "_ en un mismo día; cualquira diría que le está gustando.",
    }
    PLAYED_8_HOURS_GAME_DAY_ONE_SESSION = {
        "title": "*Mi trabajo es jugar (sin parar)*",
        "message": "Lo de estar 8 horas trabajando no suele gustar, pero jugando ya es otra cosa. "
        + "*"
        + "USER"
        + "* acaba de cascarse 8 horas seguidas (o más) jugando a _"
        + "GAME"
        + "_; cualquira diría que le está gustando.",
    }
    PLAYED_100_HOURS_GAME = {
        "title": "Una jornada laboral",
        "message": "El otro mensaje",
    }
    PLAYED_1000_HOURS = {"title": "Una jornada laboral", "message": "El otro mensaje"}
    JUST_IN_TIME = {"title": "", "message": ""}

    # Games
    PLAYED_42_GAMES = {
        "title": "*La respuesta*",
        "message": "*USER* ha jugado a la mágica cifra de 42 juegos."
        + " No sabemos si tendrá la respuesta al sentido de la vida, "
        + "al universo y todo lo demás, pero lo que seguro que tiene "
        + "es mucho tiempo libre.",
    }
    PLAYED_100_GAMES = {
        "title": "*100 juegos (jugados)*",
        "message": "A 100 juegos acaba de jugar *"
        + "USER*. Estamos hablando de arrancar un nuevo"
        + " juego cada 3,65 días (si dejara de empezar juegos). Pensemos en ello.",
    }
    COMPLETED_42_GAMES = {
        "title": "*La respuesta (de verdad)*",
        "message": "Si empezar 42 juegos ya es todo un logro, no hablemos de acabar 42. "
        + "Ha quedado patente que a *"
        + "USER"
        + "* la vida más allá de la puerta de casa no le importa lo más mínimo.",
    }
    COMPLETED_100_GAMES = {"title": "", "message": ""}
    PLAYED_5_GAMES_DAY = {"title": "", "message": ""}
    PLAYED_10_GAMES_DAY = {"title": "", "message": ""}

    # Streaks
    STREAK_7_DAYS = {"title": "", "message": ""}
    STREAK_15_DAYS = {"title": "", "message": ""}
    STREAK_30_DAYS = {"title": "", "message": ""}
    STREAK_60_DAYS = {"title": "", "message": ""}
    STREAK_100_DAYS = {"title": "", "message": ""}
    STREAK_200_DAYS = {"title": "", "message": ""}
    STREAK_300_DAYS = {"title": "", "message": ""}
    STREAK_365_DAYS = {"title": "", "message": ""}


def populate_achievements(db: Session):
    for achievement in list(Achievements):
        title = achievement.value["title"]
        message = achievement.value["message"]
        try:
            achievement = models.Achievement(title=title, message=message)
            db.add(achievement)
            db.commit()
            db.refresh(achievement)
        except SQLAlchemyError as e:
            db.rollback()
            logger.info("Error creating user: " + str(e))
            raise
        print(achievement, "->", achievement.value)


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
