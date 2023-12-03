from enum import Enum


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
