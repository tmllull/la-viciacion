import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ...config import Config
from ...database import models, schemas
from ...utils import logger
from ...utils import my_utils as utils
from ...utils.clockify_api import ClockifyApi
from . import games

clockify = ClockifyApi()
config = Config()

#################
##### USERS #####
#################


def create_admin_user(db: Session, username: str):
    try:
        db_user = (
            db.query(models.User)
            .filter(models.User.telegram_username == username)
            .first()
        )
        if db_user is None:
            db_user = models.User(telegram_username=username, is_admin=1)
            db.add(db_user)
            db.commit()
            logger.info("Admin user created")
        else:
            logger.info("Admin user already exists")
    except Exception as e:
        db.rollback()
        if "Duplicate entry" not in str(e):
            logger.info(e)


def get_users(db: Session) -> list[models.User]:
    """Get all users

    Args:
        db (Session): DB Session

    Returns:
        list[models.User]: List of all users
    """
    return db.query(models.User)


def get_user(
    db: Session, username: str, user: schemas.TelegramUser = None
) -> models.User:
    # Check tg_id
    # db_user = (
    #     db.query(models.User)
    #     .filter(models.User.telegram_id == user.telegram_id)
    #     .first()
    # )
    # if db_user is None:
    #     # Check tg_username
    db_user = (
        db.query(models.User).filter(models.User.telegram_username == username).first()
    )
    if db_user is None:
        return None
    else:
        if user is not None:
            logger.info(user)
            stmt = (
                update(models.User)
                .where(models.User.telegram_username == username)
                .values(telegram_id=user.telegram_id, name=user.telegram_name)
            )
            db.execute(stmt)
            db.commit()
            return (
                db.query(models.User)
                .filter(models.User.telegram_username == username)
                .first()
            )

    return db_user


def create_user(db: Session, username: str):
    # fake_hashed_password = user.password + "notreallyhashed"
    try:
        db_user = models.User(telegram_username=username)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        logger.info(e)


def add_new_game(
    db: Session, game: schemas.NewGameUser, user: models.User
) -> models.UsersGames:
    logger.info("Adding new user game...")
    try:
        game_db = games.get_game_by_name(db, game.game)
        user_game = models.UsersGames(
            user=user.name,
            user_id=user.id,
            completed=0,
            game=game.game,
            game_id=game_db.id,
            platform=game.platform,
            started_date=datetime.datetime.now(),
        )
        db.add(user_game)
        db.commit()
        db.refresh(user_game)
        return user_game
    except Exception as e:
        logger.info("Error adding new game user: " + str(e))
        raise Exception(e)


# def update_game(db: Session, game: models.UsersGames):
#     try:
#         stmt = (
#             update(models.UsersGames)
#             .where(
#                 models.UsersGames.game == game.game,
#                 models.UsersGames.user_id == game.user_id,
#             )
#             .values(
#                 game=game.game,
#                 platform=game.platform,
#                 score=game.score,
#                 played_time=game.played_time,
#                 # last_update=str(datetime.datetime.now()),
#             )
#         )
#         db.execute(stmt)
#         db.commit()
#         # session.close()
#     except Exception as e:
#         logger.info(e)


def update_played_time_game(db: Session, user_id: str, game: str, time: int):
    stmt = (
        update(models.UsersGames)
        .where(
            models.UsersGames.game == game,
            models.UsersGames.user_id == user_id,
        )
        .values(played_time=time)
    )
    db.execute(stmt)
    db.commit()


# def user_played_time(db: Session):
#     stmt = select(
#         models.UsersGames.player, func.sum(models.UsersGames.played_time)
#     ).group_by(models.UsersGames.player)
#     result = db.execute(stmt)
#     return result


def get_games(
    db: Session, user_id, limit=None, completed=None
) -> list[models.UsersGames]:
    if completed != None:
        completed = 1 if completed == True else 0
        return (
            db.query(models.UsersGames)
            .filter_by(user_id=user_id, completed=completed)
            .limit(limit)
        )
    else:
        return db.query(models.UsersGames).filter_by(user_id=user_id).limit(limit)


def get_game(db: Session, user_id, game) -> models.UsersGames:
    return db.query(models.UsersGames.id).filter_by(user_id=user_id, game=game).first()


def update_played_days(db: Session, user_id: int, played_days):
    try:
        stmt = (
            update(models.User)
            .where(models.User.id == user_id)
            .values(played_days=played_days)
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
        raise e


def update_played_time(db: Session, user_id, played_time):
    try:
        stmt = (
            update(models.User)
            .where(models.User.id == user_id)
            .values(played_time=played_time)
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
        raise e


def top_games(db: Session, player, limit: int = 10):
    try:
        stmt = (
            select(models.UsersGames.game, models.UsersGames.played_time)
            .where(models.UsersGames.player == player)
            .order_by(desc(models.UsersGames.played_time))
            .limit(limit)
        )
        return db.execute(stmt)
    except Exception as e:
        logger.info(e)
        raise e


# def get_achievements(db: Session, player):
#     try:
#         stmt = select(models.UserAchievements.achievement).where(
#             models.UserAchievements.player == player
#         )
#         return db.execute(stmt).fetchall()
#     except Exception as e:
#         logger.info(e)
#         raise e


def get_streaks(db: Session, player):
    try:
        return db.query(
            models.User.current_streak,
            models.User.best_streak,
            models.User.best_streak_date,
        ).filter_by(name=player)
    except Exception as e:
        logger.info(e)
        raise e


def game_completed(db: Session, player, game) -> bool:
    stmt = select(models.UsersGames).where(
        models.UsersGames.game == game,
        models.UsersGames.player == player,
        models.UsersGames.completed == 1,
    )
    game = db.execute(stmt).first()
    if game:
        return True
    return False


def complete_game(db: Session, user, game_name):
    try:
        logger.info("Completing game...")
        stmt = (
            update(models.UsersGames)
            .where(
                models.UsersGames.game == game_name, models.UsersGames.user_id == user
            )
            .values(
                completed=1,
                completed_date=datetime.datetime.now().date(),
            )
        )
        db.execute(stmt)
        db.commit()
        logger.info("Game completed")

        # completed_games_count = (
        #     db.query(models.UsersGames.game).filter_by(user=player, completed=1).count()
        # )

        return (
            db.query(models.UsersGames.game)
            .filter_by(user_id=user, completed=1)
            .count()
        )
    except Exception as e:
        db.rollback()
        raise Exception("Error completing game:", str(e))


def update_streaks(db: Session, user_id, current_streak, best_streak, best_streak_date):
    try:
        logger.info("Update streaks...")
        stmt = (
            update(models.User)
            .where(models.User.id == user_id)
            .values(
                current_streak=current_streak,
                best_streak=best_streak,
                best_streak_date=best_streak_date,
            )
        )
        db.execute(stmt)
        db.commit()

        # completed_games_count = (
        #     db.query(models.UsersGames.game).filter_by(user=player, completed=1).count()
        # )
    except Exception as e:
        db.rollback()
        logger.info(e)
        raise Exception("Error updating streaks:", str(e))


# def set_user_achievement(db: Session, player, achievement):
#     try:
#         ach = models.UserAchievements(player=player, achievement=achievement)
#         db.add(ach)
#         db.commit()
#         return False
#     except Exception as e:
#         db.rollback()
#         if "Duplicate entry" in str(e) or "UNIQUE" in str(e):
#             # logger.info("Logro '" + achievement + "' ya desbloqueado")
#             return True
#         else:
#             raise Exception("Error checking achievement:", e)


def get_most_played_time(db: Session, limit: int = None) -> list[models.User]:
    if limit is not None:
        return (
            db.query(models.User).order_by(desc(models.User.played_time)).limit(limit)
        )
    else:
        return db.query(models.User).order_by(desc(models.User.played_time))
