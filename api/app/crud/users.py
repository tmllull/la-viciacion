import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, or_, select, text, update
from sqlalchemy.orm import Session

from ..config import Config
from ..database import models, schemas
from ..utils import logger
from ..utils import my_utils as utils
from ..utils.clockify_api import ClockifyApi
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


def get_user(db: Session, username: str) -> models.User:
    db_user = (
        db.query(models.User).filter(models.User.telegram_username == username).first()
    )
    if db_user is None:
        return None
    return db_user


def create_user(db: Session, user: schemas.UserAddOrUpdate) -> models.User:
    try:
        db_user = models.User(
            name=user.name,
            telegram_username=user.telegram_username,
            telegram_id=user.telegram_id,
            clockify_id=user.clockify_id,
            is_admin=user.is_admin,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return (
            db.query(models.User)
            .filter(models.User.telegram_username == user.telegram_username)
            .first()
        )
    except Exception as e:
        logger.info(e)


def update_user(db: Session, user: schemas.UserAddOrUpdate):
    try:
        logger.info(user)
        db_user = get_user(db, user.telegram_username)
        name = user.name if user.name is not None else db_user.name
        telegram_id = (
            user.telegram_id if user.telegram_id is not None else db_user.telegram_id
        )
        is_admin = user.is_admin if user.is_admin is not None else db_user.is_admin
        clockify_id = (
            user.clockify_id if user.clockify_id is not None else db_user.clockify_id
        )
        stmt = (
            update(models.User)
            .where(models.User.telegram_username == user.telegram_username)
            .values(
                telegram_id=telegram_id,
                name=name,
                is_admin=is_admin,
                clockify_id=clockify_id,
            )
        )
        db.execute(stmt)
        db.commit()
        return (
            db.query(models.User)
            .filter(models.User.telegram_username == user.telegram_username)
            .first()
        )
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


def update_game(db: Session, game: schemas.UsersGames, entry_id):
    try:
        stmt = (
            update(models.UsersGames)
            .where(
                models.UsersGames.id == entry_id,
                or_(
                    models.UsersGames.platform == "TBD",
                    models.UsersGames.platform == None,
                ),
            )
            .values(platform=game.platform)
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
        raise e


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
    return db.query(models.UsersGames).filter_by(user_id=user_id, game=game).first()


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


def complete_game(db: Session, user_id, game_name):
    try:
        logger.info("Completing game...")
        stmt = (
            update(models.UsersGames)
            .where(
                models.UsersGames.game == game_name,
                models.UsersGames.user_id == user_id,
            )
            .values(
                completed=1,
                completed_date=datetime.datetime.now().date(),
            )
        )
        db.execute(stmt)
        db.commit()
        logger.info("Game completed")
        num_completed_games = (
            db.query(models.UsersGames.game)
            .filter_by(user_id=user_id, completed=1)
            .count()
        )
        user_game = get_game(db, user_id, game_name)
        logger.info(user_game.completion_time)
        completion_time = user_game.completion_time
        return num_completed_games, completion_time

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
    except Exception as e:
        db.rollback()
        logger.info(e)
        raise Exception("Error updating streaks:", str(e))


def get_most_played_time(db: Session, limit: int = None) -> list[models.User]:
    if limit is not None:
        return (
            db.query(models.User).order_by(desc(models.User.played_time)).limit(limit)
        )
    else:
        return db.query(models.User).order_by(desc(models.User.played_time))
