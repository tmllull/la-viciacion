import datetime
import json
from typing import Tuple, Union

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

clockify_api = ClockifyApi()
config = Config()

#################
##### USERS #####
#################


def create_admin_user(db: Session, username: str):
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
        else:
            logger.warning(username + " already exists as admin")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error creating admin user: " + str(e))
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
        logger.error("Error getting users: " + str(e))
        raise


def is_admin(db: Session, username: str) -> models.User:
    try:
        return (
            db.query(models.User)
            .filter(models.User.username == username, models.User.is_admin == 1)
            .first()
        )
    except SQLAlchemyError as e:
        logger.error("Error checking is user is admin: " + str(e))
        raise


def is_active(db: Session, username: str) -> models.User:
    try:
        return (
            db.query(models.User)
            .filter(models.User.username == username, models.User.is_active == 1)
            .first()
        )
    except SQLAlchemyError as e:
        logger.error("Error checking is user is active: " + str(e))
        raise


def get_user_by_username(db: Session, username: str) -> models.User:
    try:
        return db.query(models.User).filter(models.User.username == username).first()
    except SQLAlchemyError as e:
        logger.error("Error getting user by username: " + str(e))
        raise


def get_user_by_id(db: Session, id: int) -> models.User:
    try:
        return db.query(models.User).filter(models.User.id == id).first()
    except SQLAlchemyError as e:
        logger.error("Error getting user by id: " + str(e))
        raise


def create_user(
    db: Session, user: schemas.UserCreate
) -> Union[Tuple[bool, models.User], Tuple[bool, int]]:
    # generating the salt
    salt = bcrypt.gensalt()

    # Check password length and email format
    if not utils.validate_email_format(user.email):
        return (False, 1)
    if not utils.validate_password_requirements(user.password):
        return (False, 0)

    # Hashing the password
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)

    try:
        db_user = models.User(
            username=user.username, password=hashed_password, email=user.email
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        try:
            user_statistics = models.UserStatistics(
                user_id=db_user.id, current_ranking_hours=1000
            )
            db.add(user_statistics)
            db.commit()
        except Exception as e:
            db.rollback()
            if "Duplicate" not in str(e):
                #     db.rollback()
                # else:
                logger.error("Error adding new game statistics: " + str(e))
                raise e
            else:
                logger.warning("User already exists in DB")
        # db.refresh(user_statistics)
        return True, db_user

        # return (
        #     db.query(models.User).filter(models.User.username == user.username).first()
        # )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error creating user: " + str(e))
        raise


def create_user_statistics(db: Session, user_id: id):
    try:
        user_statistics = models.UserStatistics(
            user_id=user_id, current_ranking_hours=1000
        )
        db.add(user_statistics)
        db.commit()
        db.refresh(user_statistics)

    except SQLAlchemyError as e:
        db.rollback()
        if "Duplicate" not in str(e):
            logger.error("Error creating user statistics: " + str(e))
            raise e


def update_user(db: Session, user: schemas.UserUpdate):
    try:
        # logger.info(user)
        db_user = get_user_by_username(db, user.username)
        name = user.name if user.name is not None else db_user.name
        # username = user.username if user.username is not None else db_user.username
        email = user.email if user.email is not None else db_user.email
        telegram_id = (
            user.telegram_id if user.telegram_id is not None else db_user.telegram_id
        )
        clockify_id = (
            user.clockify_id if user.clockify_id is not None else db_user.clockify_id
        )
        clockify_key = (
            user.clockify_key if user.clockify_key is not None else db_user.clockify_key
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
                email=email,
                password=password,
                clockify_id=clockify_id,
                clockify_key=clockify_key,
            )
        )
        db.execute(stmt)
        db.commit()
        return (
            db.query(models.User).filter(models.User.username == user.username).first()
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error updating user: " + str(e))
        raise


def update_user_as_admin(db: Session, user: schemas.UserUpdateForAdmin):
    try:
        # logger.info(user)
        db_user = get_user_by_username(db, user.username)
        name = user.name if user.name is not None else db_user.name
        # username = user.username if user.username is not None else db_user.username
        email = user.email if user.email is not None else db_user.email
        telegram_id = (
            user.telegram_id if user.telegram_id is not None else db_user.telegram_id
        )
        is_admin = user.is_admin if user.is_admin is not None else db_user.is_admin
        is_active = user.is_active if user.is_active is not None else db_user.is_active
        clockify_id = (
            user.clockify_id if user.clockify_id is not None else db_user.clockify_id
        )
        clockify_key = (
            user.clockify_key if user.clockify_key is not None else db_user.clockify_key
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
                email=email,
                is_admin=is_admin,
                is_active=is_active,
                password=password,
                clockify_id=clockify_id,
                clockify_key=clockify_key,
            )
        )
        db.execute(stmt)
        db.commit()
        return (
            db.query(models.User).filter(models.User.username == user.username).first()
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error updating user: " + str(e))
        raise


def update_user_telegram_id(db: Session, user: schemas.TelegramUser):
    try:
        stmt = (
            update(models.User)
            .where(models.User.username == user.username)
            .values(
                telegram_id=user.telegram_id,
            )
        )
        db.execute(stmt)
        db.commit()
        return (
            db.query(models.User).filter(models.User.username == user.username).first()
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error updating TelegramID user: " + str(e))
        raise


def update_clockify_id(db: Session, username: str, user_clockify):
    if user_clockify is not None:
        try:
            clockify_id = user_clockify["id"]
            stmt = (
                update(models.User)
                .where(models.User.username == username)
                .values(
                    clockify_id=clockify_id,
                )
            )
            db.execute(stmt)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error("Error updating user clockify_id: " + str(e))
            raise

    else:
        logger.info("User nor found in Clockify")


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
        logger.error("Error adding avatar: " + str(e))
        raise


def get_avatar(db: Session, username: str):
    try:
        return (
            db.query(models.User.avatar)
            .filter(models.User.username == username)
            .first()
        )
    except SQLAlchemyError as e:
        logger.error("Error getting avatar: " + str(e))
        raise


async def add_new_game(
    db: Session,
    game: schemas.NewGameUser,
    user: models.User,
    start_date: str = None,
    silent: bool = False,
    from_sync=False,
) -> models.UserGame:
    logger.info("Adding new user game...")
    try:
        if start_date is None:
            started_date = datetime.datetime.now()
        else:
            started_date = utils.convert_date_from_text(start_date)
        game_db = games.get_game_by_id(db, game.game_id)
        if game_db is None:
            return None
        # info_game = await utils.get_game_info(game_db.name)
        user_game = models.UserGame(
            game_id=game_db.id,
            user_id=user.id,
            completed=0,
            # project_clockify_id=game_db.clockify_id,
            platform=game.platform,
            started_date=started_date,
        )
        db.add(user_game)
        db.commit()
        db.refresh(user_game)
        played_games = get_games(db, user.id).count()
        if not from_sync:
            clockify_api.create_empty_time_entry(
                db, user.clockify_key, game_db.id, game.platform
            )
        started_game = (
            "[" + game_db.name + "](https://rawg.io/games/" + game_db.slug + ")\n"
        )
        await utils.send_message(
            user.name
            + " acaba de empezar su juego número "
            + str(played_games)
            + ": "
            + started_game,
            silent,
        )
        logger.info("Game added!")
        return user_game
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error adding new game user: " + str(e))
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
        logger.error("Error updating game: " + str(e))
        raise


def update_played_time_game(db: Session, user_id: str, game_id: str, time: int):
    try:
        stmt = (
            update(models.UserGame)
            .where(
                models.UserGame.game_id == game_id,
                models.UserGame.user_id == user_id,
            )
            .values(played_time=time)
        )
        db.execute(stmt)
        db.commit()
        # TODO: Check games time achievements
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error updating played time game: " + str(e))
        raise


def get_games(
    db: Session, user_id, limit=None, completed=None
) -> list[schemas.UserGame]:
    if completed != None:
        completed = 1 if completed == True else 0
        stmt = (
            select(
                models.UserGame.__table__,
                # models.Game.name.label("game_name"),
                # models.PlatformTag.name.label("platform_name"),
            )
            # .join(models.Game, models.UserGame.game_id == models.Game.id)
            # .join(models.PlatformTag, models.UserGame.platform == models.PlatformTag.id)
            .where(
                models.UserGame.user_id == user_id,
                models.UserGame.completed == completed,
            ).limit(limit)
        )
        return db.execute(stmt).fetchall()

    else:
        stmt = (
            select(
                models.UserGame.__table__,
                # models.Game.name.label("game_name"),
                # models.PlatformTag.name.label("platform_name"),
            )
            # .join(models.Game, models.UserGame.game_id == models.Game.id)
            # .join(models.PlatformTag, models.UserGame.platform == models.PlatformTag.id)
            .where(models.UserGame.user_id == user_id).limit(limit)
        )
        return db.execute(stmt).fetchall()
    # stmt = (
    #     select(
    #         models.UserGame.__table__,
    #         models.Game.name.label("game_name"),
    #         models.PlatformTag.name.label("platform_name"),
    #     )
    #     .join(models.Game, models.UserGame.game_id == models.Game.id)
    #     .join(models.PlatformTag, models.UserGame.platform == models.PlatformTag.id)
    #     .where(
    #         models.UserGame.user_id == user_id,
    #         models.UserGame.completed
    #         == ((1 if completed else 0) if completed is not None else True),
    #     )
    #     .limit(limit)
    # )

    # return db.execute(stmt).fetchall()


def get_game_by_id(db: Session, user_id, game_id) -> models.UserGame:
    return db.query(models.UserGame).filter_by(user_id=user_id, game_id=game_id).first()


# def get_game_by_clockify_id(
#     db: Session, user_id, project_clockify_id
# ) -> models.UserGame:
#     return (
#         db.query(models.UserGame)
#         .filter_by(user_id=user_id, project_clockify_id=project_clockify_id)
#         .first()
#     )


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
        logger.error(e)
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
        logger.error(e)
        raise e


def top_games(db: Session, username: str, limit: int = 10):
    try:
        user = get_user_by_username(db, username)
        stmt = (
            select(
                models.UserGame.user_id,
                models.UserGame.game_id,
                models.Game.name,
                models.User.name,
                models.UserGame.played_time.label("total_played_time"),
            )
            .join(models.User, models.User.id == models.UserGame.user_id)
            .join(models.Game, models.Game.id == models.UserGame.game_id)
            .where(models.UserGame.user_id == user.id)
            .group_by(
                models.UserGame.user_id,
                models.UserGame.game_id,
                models.Game.name,
                models.User.name,
                models.UserGame.played_time,
            )
            .order_by(desc(models.UserGame.played_time))
            .limit(limit)
        )
        return db.execute(stmt).fetchall()

        # stmt = (
        #     select(models.UserGame.game_id, models.UserGame.played_time)
        #     .where(models.UserGame. == player)
        #     .order_by(desc(models.UserGame.played_time))
        #     .limit(limit)
        # )
        # return db.execute(stmt)
    except Exception as e:
        logger.error(e)
        raise e


def get_streaks(db: Session, player):
    try:
        return db.query(
            models.UserStatistics.current_streak,
            models.UserStatistics.best_streak,
            models.UserStatistics.best_streak_date,
        ).filter_by(name=player)
    except Exception as e:
        logger.error(e)
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


async def complete_game(
    db: Session,
    user_id,
    game_id,
    completed_date: str = None,
    silent: bool = False,
    from_sync=False,
):
    try:
        if completed_date is None:
            completed_date = datetime.datetime.now()
        else:
            completed_date = utils.convert_date_from_text(completed_date)
        stmt = (
            update(models.UserGame)
            .where(
                models.UserGame.game_id == game_id,
                models.UserGame.user_id == user_id,
            )
            .values(
                completed=1,
                completed_date=completed_date,
            )
        )
        db.execute(stmt)
        db.commit()
        logger.info("Game completed")
        db_game = games.get_game_by_id(db, game_id)
        user = get_user_by_id(db, user_id)
        user_game = get_game_by_id(db, user_id, db_game.id)
        game_info = await utils.get_game_info(db_game.name)
        if game_info["hltb"] is not None:
            avg_time = game_info["hltb"]["comp_main"]
        else:
            avg_time = 0
        games.update_avg_time_game(db, game_id, avg_time)
        game = games.get_game_by_id(db, game_id)
        if not from_sync:
            clockify_response = clockify_api.create_empty_time_entry(
                db,
                user.clockify_key,
                game_id,
                user_game.platform,
                completed=True,
            )
        num_completed_games = (
            db.query(models.UserGame.game_id)
            .filter_by(user_id=user_id, completed=1)
            .count()
        )
        completion_time = user_game.completion_time
        message = (
            user.name
            + " acaba de completar su juego número "
            + str(num_completed_games)
            + ": *"
            + game.name
            + "* en "
            + str(utils.convert_time_to_hours(completion_time))
            + ". La media está en "
            + str(utils.convert_time_to_hours(avg_time))
            + "."
        )
        logger.info(message)
        await utils.send_message(message, silent)
        return get_game_by_id(db, user_id, game_id)
        # num_completed_games = (
        #     db.query(models.UserGame.game_id)
        #     .filter_by(user_id=user_id, completed=1)
        #     .count()
        # )
        # user_game = get_game_by_id(db, user_id, game_id)
        # completion_time = user_game.completion_time
        # return num_completed_games, completion_time

    except Exception as e:
        db.rollback()
        logger.error("Error completing game: " + str(e))
        raise e


async def rate_game(
    db: Session,
    user_id,
    game_id,
    score,
) -> models.UserGame:
    try:
        stmt = (
            update(models.UserGame)
            .where(
                models.UserGame.game_id == game_id,
                models.UserGame.user_id == user_id,
            )
            .values(
                score=score,
            )
        )
        db.execute(stmt)
        db.commit()
        return get_game_by_id(db, user_id, game_id)
        logger.info("Game completed")

    except Exception as e:
        db.rollback()
        logger.error("Error rating game: " + str(e))
        raise e


def update_streaks(db: Session, user_id, current_streak, best_streak, best_streak_date):
    try:
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
        logger.error("Error updating streaks: " + str(e))
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
        logger.error("Error getting current ranking hours: " + str(e))


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
        logger.error("Error activating account: " + str(e))
        raise e
