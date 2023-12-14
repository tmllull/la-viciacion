import datetime
from enum import Enum

from sqlalchemy import update
from sqlalchemy.orm import Session

from ..database import models
from . import my_utils as utils


class AchievementsElems(Enum):
    # Format -> KEY = {"title":"", "message":""}
    # Time day
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
    PLAYED_100_HOURS = {"title": "PLAYED_100_HOURS", "message": ""}
    PLAYED_200_HOURS = {"title": "PLAYED_200_HOURS", "message": ""}
    PLAYED_500_HOURS = {"title": "PLAYED_500_HOURS", "message": ""}
    PLAYED_1000_HOURS = {"title": "PLAYED_1000_HOURS", "message": ""}

    # Session time
    PLAYED_LESS_5_MIN_SESSION = {"title": "Lo he abierto sin querer", "message": "###"}
    PLAYED_4_HOURS_SESSION = {"title": "PLAYED_4HOURS_SESSION", "message": ""}
    PLAYED_8_HOURS_SESSION = {"title": "PLAYED_8HOURS_SESSION", "message": ""}

    # Games
    PLAYED_10_GAMES = {
        "title": "PLAYED_10_GAMES",
        "message": "",
    }
    PLAYED_42_GAMES = {
        "title": "La respuesta",
        "message": "USER ha jugado a la mágica cifra de 42 juegos."
        + " No sabemos si tendrá la respuesta al sentido de la vida, "
        + "al universo y todo lo demás, pero lo que seguro que tiene "
        + "es mucho tiempo libre.",
    }
    PLAYED_50_GAMES = {
        "title": "PLAYED_50_GAMES",
        "message": "",
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
    COMPLETED_100_GAMES = {"title": "COMPLETED_100_GAMES", "message": ""}
    PLAYED_5_GAMES_DAY = {"title": "PLAYED_5_GAMES_DAY", "message": ""}
    PLAYED_10_GAMES_DAY = {"title": "PLAYED_10_GAMES_DAY", "message": ""}

    # Total days
    PLAYED_7_DAYS = {"title": "PLAYED_7_DAYS", "message": ""}
    PLAYED_15_DAYS = {"title": "PLAYED_15_DAYS", "message": ""}
    PLAYED_30_DAYS = {"title": "PLAYED_30_DAYS", "message": ""}
    PLAYED_60_DAYS = {"title": "PLAYED_60_DAYS", "message": ""}
    PLAYED_100_DAYS = {"title": "PLAYED_100_DAYS", "message": ""}
    PLAYED_200_DAYS = {"title": "PLAYED_200_DAYS", "message": ""}
    PLAYED_300_DAYS = {"title": "PLAYED_300_DAYS", "message": ""}
    PLAYED_365_DAYS = {"title": "PLAYED_365_DAYS", "message": ""}

    # Streaks
    STREAK_7_DAYS = {"title": "STREAK_7_DAYS", "message": ""}
    STREAK_15_DAYS = {"title": "STREAK_15_DAYS", "message": ""}
    STREAK_30_DAYS = {"title": "STREAK_30_DAYS", "message": ""}
    STREAK_60_DAYS = {"title": "STREAK_60_DAYS", "message": ""}
    STREAK_100_DAYS = {"title": "STREAK_100_DAYS", "message": ""}
    STREAK_200_DAYS = {"title": "STREAK_200_DAYS", "message": ""}
    STREAK_300_DAYS = {"title": "STREAK_300_DAYS", "message": ""}
    STREAK_365_DAYS = {"title": "STREAK_365_DAYS", "message": ""}

    # Others
    JUST_IN_TIME = {"title": "Justo a tiempo", "message": ""}
