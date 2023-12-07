import datetime
from typing import Union

import bcrypt
from sqlalchemy import asc, create_engine, desc, func, or_, select, text, update
from sqlalchemy.exc import SQLAlchemyError
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
    logger.info("Creating admin users")
    try:
        db_user = db.query(models.User).filter(models.User.username == username).first()
        if db_user is None:
            salt = bcrypt.gensalt()
            default_password = "admin"
            # Hashing the password
            hashed_password = bcrypt.hashpw(default_password.encode("utf-8"), salt)
            db_user = models.User(
                username=username, is_admin=1, password=hashed_password, is_active=1
            )
            db.add(db_user)
            db.commit()
            logger.info("Admin user created")
    except SQLAlchemyError as e:
        db.rollback()
        logger.info("Error creating admin user: " + str(e))
        if "Duplicate entry" not in str(e):
            logger.info(e)
        else:
            raise


def get_users(db: Session) -> list[models.User]:
    """Get all users

    Args:
        db (Session): DB Session

    Returns:
        list[models.User]: List of all users
    """
    try:
        return db.query(models.User)
    except SQLAlchemyError as e:
        logger.info("Error getting users: " + str(e))
        raise


def is_admin(db: Session, username: str) -> models.User:
    try:
        return (
            db.query(models.User)
            .filter(models.User.username == username, models.User.is_admin == 1)
            .first()
        )
    except SQLAlchemyError as e:
        logger.info("Error checking is user is admin: " + str(e))
        raise


def is_active(db: Session, username: str) -> models.User:
    try:
        return (
            db.query(models.User)
            .filter(models.User.username == username, models.User.is_active == 1)
            .first()
        )
    except SQLAlchemyError as e:
        logger.info("Error checking is user is active: " + str(e))
        raise


def get_user_by_username(db: Session, username: str) -> models.User:
    try:
        return db.query(models.User).filter(models.User.username == username).first()
    except SQLAlchemyError as e:
        logger.info("Error getting user by username: " + str(e))
        raise


def get_user_by_id(db: Session, id: int) -> models.User:
    try:
        return db.query(models.User).filter(models.User.id == id).first()
    except SQLAlchemyError as e:
        logger.info("Error getting user by id: " + str(e))
        raise


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)

    try:
        db_user = models.User(username=user.username, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return (
            db.query(models.User).filter(models.User.username == user.username).first()
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.info("Error creating user: " + str(e))
        raise


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
            update(models.User)
            .where(models.User.username == user.username)
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
            db.query(models.User).filter(models.User.username == user.username).first()
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.info("Error updating user: " + str(e))
        raise


def upload_avatar(db: Session, username: str, avatar: bytes):
    try:
        stmt = (
            update(models.User)
            .where(models.User.username == username)
            .values(avatar=avatar)
        )
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.info("Error adding avatar: " + str(e))
        raise


def get_avatar(db: Session, username: str):
    try:
        return (
            db.query(models.User.avatar)
            .filter(models.User.username == username)
            .first()
        )
    except SQLAlchemyError as e:
        logger.info("Error getting avatar: " + str(e))
        raise


def add_new_game(
    db: Session, game: schemas.NewGameUser, user: models.User
) -> models.UserGame:
    logger.info("Adding new user game...")
    try:
        game_db = games.get_game_by_clockify_id(db, game.project_clockify_id)
        user_game = models.UserGame(
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
        logger.info("Game added!")
        return user_game
    except SQLAlchemyError as e:
        db.rollback()
        logger.info("Error adding new game user: " + str(e))
        raise


def update_game(db: Session, game: schemas.UserGame, entry_id):
    try:
        stmt = (
            update(models.UserGame)
            .where(
                models.UserGame.id == entry_id,
                or_(
                    models.UserGame.platform == "TBD",
                    models.UserGame.platform == None,
                ),
            )
            .values(platform=game.platform)
        )
        db.execute(stmt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.info("Error updating game: " + str(e))
        raise


def update_played_time_game(db: Session, user_id: str, game: str, time: int):
    try:
        stmt = (
            update(models.UserGame)
            .where(
                models.UserGame.project_clockify_id == game,
                models.UserGame.user_id == user_id,
            )
            .values(played_time=time)
        )
        db.execute(stmt)
        db.commit()
        # TODO: Check games time achievements
    except SQLAlchemyError as e:
        db.rollback()
        logger.info("Error updating played time game: " + str(e))
        raise


def get_games(
    db: Session, user_id, limit=None, completed=None
) -> list[models.UserGame]:
    if completed != None:
        completed = 1 if completed == True else 0
        games_list = (
            db.query(models.UserGame)
            .filter_by(user_id=user_id, completed=completed)
            .limit(limit)
        )
        return games_list
    else:
        games_list = db.query(models.UserGame).filter_by(user_id=user_id).limit(limit)
        return games_list


def get_game_by_id(db: Session, user_id, game_id) -> models.UserGame:
    return db.query(models.UserGame).filter_by(user_id=user_id, game_id=game_id).first()


def get_game_by_clockify_id(
    db: Session, user_id, project_clockify_id
) -> models.UserGame:
    return (
        db.query(models.UserGame)
        .filter_by(user_id=user_id, project_clockify_id=project_clockify_id)
        .first()
    )


def update_played_days(db: Session, user_id: int, played_days):
    try:
        stmt = (
            update(models.UserStatistics)
            .where(models.UserStatistics.user_id == user_id)
            .values(played_days=played_days)
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.info(e)
        raise e


def update_played_time(db: Session, user_id, played_time):
    try:
        stmt = (
            update(models.UserStatistics)
            .where(models.UserStatistics.user_id == user_id)
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
            select(models.UserGame.game, models.UserGame.played_time)
            .where(models.UserGame.player == player)
            .order_by(desc(models.UserGame.played_time))
            .limit(limit)
        )
        return db.execute(stmt)
    except Exception as e:
        logger.info(e)
        raise e


def get_streaks(db: Session, player):
    try:
        return db.query(
            models.UserStatistics.current_streak,
            models.UserStatistics.best_streak,
            models.UserStatistics.best_streak_date,
        ).filter_by(name=player)
    except Exception as e:
        logger.info(e)
        raise e


def game_is_completed(db: Session, player, game) -> bool:
    stmt = select(models.UserGame).where(
        models.UserGame.game == game,
        models.UserGame.player == player,
        models.UserGame.completed == 1,
    )
    game = db.execute(stmt).first()
    if game:
        return True
    return False


def complete_game(db: Session, user_id, game_id):
    try:
        logger.info("Completing game...")
        stmt = (
            update(models.UserGame)
            .where(
                models.UserGame.game_id == game_id,
                models.UserGame.user_id == user_id,
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
            db.query(models.UserGame.game_id)
            .filter_by(user_id=user_id, completed=1)
            .count()
        )
        user_game = get_game_by_id(db, user_id, game_id)
        completion_time = user_game.completion_time
        return num_completed_games, completion_time

    except Exception as e:
        db.rollback()
        raise e


def update_streaks(db: Session, user_id, current_streak, best_streak, best_streak_date):
    try:
        logger.info("Update streaks...")
        stmt = (
            update(models.UserStatistics)
            .where(models.UserStatistics.user_id == user_id)
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
        raise e


def played_time(db: Session, limit: int = None) -> list[models.UserStatistics]:
    return (
        db.query(models.UserStatistics)
        .order_by(desc(models.UserStatistics.played_time))
        .limit(limit)
    )


def played_days(db: Session, limit: int = None) -> list[models.UserStatistics]:
    return (
        db.query(models.UserStatistics)
        .order_by(desc(models.UserStatistics.played_days))
        .limit(limit)
    )


def current_ranking_hours(
    db: Session, limit: int = None
) -> list[models.UserStatistics]:
    try:
        return (
            db.query(models.UserStatistics)
            .order_by(asc(models.UserStatistics.current_ranking_hours))
            .limit(limit)
        )
    except Exception as e:
        logger.info(e)


def update_current_ranking_hours(db: Session, ranking, user_id):
    stmt = (
        update(models.UserStatistics)
        .where(models.UserStatistics.user_id == user_id)
        .values(current_ranking_hours=ranking)
    )
    db.execute(stmt)
    db.commit()


def activate_account(db: Session, username: str):
    try:
        logger.info("Activating account...")
        db_user = (
            db.query(models.User)
            .filter(models.User.username == username, models.User.is_active == 1)
            .first()
        )
        if db_user:
            return False
        stmt = (
            update(models.User)
            .where(models.User.username == username)
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
        raise e
