import datetime
from typing import Union

import bcrypt
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
            db.query(models.Users).filter(models.Users.username == username).first()
        )
        if db_user is None:
            salt = bcrypt.gensalt()
            default_password = "admin"
            # Hashing the password
            hashed_password = bcrypt.hashpw(default_password.encode("utf-8"), salt)
            db_user = models.Users(
                username=username, is_admin=1, password=hashed_password, is_active=1
            )
            db.add(db_user)
            db.commit()
            logger.info("Admin user created")
        else:
            logger.info("Admin user already exists")
    except Exception as e:
        db.rollback()
        if "Duplicate entry" not in str(e):
            logger.info(e)


def get_users(db: Session) -> list[models.Users]:
    """Get all users

    Args:
        db (Session): DB Session

    Returns:
        list[models.User]: List of all users
    """
    return db.query(models.Users)


def is_admin(db: Session, username: str) -> models.Users:
    return (
        db.query(models.Users)
        .filter(models.Users.username == username, models.Users.is_admin == 1)
        .first()
    )


def is_active(db: Session, username: str) -> models.Users:
    return (
        db.query(models.Users)
        .filter(models.Users.username == username, models.Users.is_active == 1)
        .first()
    )


def get_user_by_username(db: Session, username: str) -> models.Users:
    return db.query(models.Users).filter(models.Users.username == username).first()


def get_user_by_id(db: Session, id: int) -> models.Users:
    return db.query(models.Users).filter(models.Users.id == id).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.Users:
    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)

    try:
        db_user = models.Users(username=user.username, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return (
            db.query(models.Users)
            .filter(models.Users.username == user.username)
            .first()
        )
    except Exception as e:
        logger.info(e)


def update_user(db: Session, user: schemas.UserUpdate):
    try:
        logger.info(user)
        db_user = get_user_by_username(db, user.username)
        name = user.name if user.name is not None else db_user.name
        telegram_id = (
            user.telegram_id if user.telegram_id is not None else db_user.telegram_id
        )
        is_admin = user.is_admin if user.is_admin is not None else db_user.is_admin
        clockify_id = (
            user.clockify_id if user.clockify_id is not None else db_user.clockify_id
        )
        if user.password is not None:
            salt = bcrypt.gensalt()

            # Hashing the password
            hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
            password = hashed_password
        else:
            password = db_user.password
        stmt = (
            update(models.Users)
            .where(models.Users.username == user.username)
            .values(
                telegram_id=telegram_id,
                name=name,
                is_admin=is_admin,
                password=password,
                clockify_id=clockify_id,
            )
        )
        db.execute(stmt)
        db.commit()
        return (
            db.query(models.Users)
            .filter(models.Users.username == user.username)
            .first()
        )
    except Exception as e:
        logger.info(e)


def upload_avatar(db: Session, username: str, avatar: bytes):
    try:
        stmt = (
            update(models.Users)
            .where(models.Users.username == username)
            .values(avatar=avatar)
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
        raise Exception(e)


def get_avatar(db: Session, username: str):
    try:
        return (
            db.query(models.Users.avatar)
            .filter(models.Users.username == username)
            .first()
        )
    except Exception as e:
        logger.info(e)


def add_new_game(
    db: Session, game: schemas.NewGameUser, user: models.Users
) -> models.UsersGames:
    logger.info("Adding new user game...")
    try:
        game_db = games.get_game_by_clockify_id(db, game.project_clockify_id)
        user_game = models.UsersGames(
            user_id=user.id,
            completed=0,
            game_id=game_db.id,
            project_clockify_id=game_db.clockify_id,
            platform=game.platform,
            started_date=datetime.datetime.now(),
        )
        db.add(user_game)
        db.commit()
        db.refresh(user_game)
        return user_game
    except Exception as e:
        db.rollback()
        logger.info("Error adding new game user: " + str(e))
        raise Exception("Error adding new game user: " + str(e))


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
            models.UsersGames.project_clockify_id == game,
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
        games_list = (
            db.query(models.UsersGames)
            .filter_by(user_id=user_id, completed=completed)
            .limit(limit)
        )
        return games_list
    else:
        games_list = db.query(models.UsersGames).filter_by(user_id=user_id).limit(limit)
        return games_list


def get_game_by_id(db: Session, user_id, game_id) -> models.UsersGames:
    return (
        db.query(models.UsersGames).filter_by(user_id=user_id, game_id=game_id).first()
    )


def get_game_by_clockify_id(
    db: Session, user_id, project_clockify_id
) -> models.UsersGames:
    return (
        db.query(models.UsersGames)
        .filter_by(user_id=user_id, project_clockify_id=project_clockify_id)
        .first()
    )


def update_played_days(db: Session, user_id: int, played_days):
    try:
        stmt = (
            update(models.Users)
            .where(models.Users.id == user_id)
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
            update(models.Users)
            .where(models.Users.id == user_id)
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
            models.Users.current_streak,
            models.Users.best_streak,
            models.Users.best_streak_date,
        ).filter_by(name=player)
    except Exception as e:
        logger.info(e)
        raise e


def game_is_completed(db: Session, player, game) -> bool:
    stmt = select(models.UsersGames).where(
        models.UsersGames.game == game,
        models.UsersGames.player == player,
        models.UsersGames.completed == 1,
    )
    game = db.execute(stmt).first()
    if game:
        return True
    return False


def complete_game(db: Session, user_id, game_id):
    try:
        logger.info("Completing game...")
        stmt = (
            update(models.UsersGames)
            .where(
                models.UsersGames.game_id == game_id,
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
            db.query(models.UsersGames.game_id)
            .filter_by(user_id=user_id, completed=1)
            .count()
        )
        user_game = get_game_by_id(db, user_id, game_id)
        completion_time = user_game.completion_time
        return num_completed_games, completion_time

    except Exception as e:
        db.rollback()
        raise Exception("Error completing game:", str(e))


def update_streaks(db: Session, user_id, current_streak, best_streak, best_streak_date):
    try:
        logger.info("Update streaks...")
        stmt = (
            update(models.Users)
            .where(models.Users.id == user_id)
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


def played_time(db: Session, limit: int = None) -> list[models.Users]:
    return db.query(models.Users).order_by(desc(models.Users.played_time)).limit(limit)


def played_days(db: Session, limit: int = None) -> list[models.Users]:
    return db.query(models.Users).order_by(desc(models.Users.played_days)).limit(limit)


def current_ranking_hours(db: Session, limit: int = None) -> list[models.Users]:
    try:
        return (
            db.query(models.Users)
            .order_by(asc(models.Users.current_ranking_hours))
            .limit(limit)
        )
    except Exception as e:
        logger.info(e)


def update_current_ranking_hours(db: Session, ranking, user_id):
    stmt = (
        update(models.Users)
        .where(models.Users.id == user_id)
        .values(current_ranking_hours=ranking)
    )
    db.execute(stmt)
    db.commit()


def activate_account(db: Session, username: str):
    try:
        logger.info("Activating account...")
        db_user = (
            db.query(models.Users)
            .filter(models.Users.username == username, models.Users.is_active == 1)
            .first()
        )
        if db_user:
            return False
        stmt = (
            update(models.Users)
            .where(models.Users.username == username)
            .values(
                is_active=1,
            )
        )
        db.execute(stmt)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.info(e)
        raise Exception("Error activating account:", str(e))
