import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ...database import models, schemas
from ...utils import logger
from ...utils import my_utils as utils
from ...utils.clockify_api import ClockifyApi
from . import games

clockify = ClockifyApi()

#################
##### USERS #####
#################


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


# def get_user(db: Session, user_id: int) -> models.User:
#     return db.query(models.User).filter(models.User.id == user_id).first()


def get_user(db: Session, user: Union[int, str]) -> models.User:
    # Check ID
    db_user = db.query(models.User).filter(models.User.id == user).first()
    # Check tg_id
    if db_user is None:
        db_user = db.query(models.User).filter(models.User.telegram_id == user).first()
        if db_user is None:
            # Check tg_username
            db_user = (
                db.query(models.User)
                .filter(models.User.telegram_username == user)
                .first()
            )
            if db_user is None:
                return None
    return db_user


def create_user(db: Session, user: schemas.User):
    # fake_hashed_password = user.password + "notreallyhashed"
    # db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    # db.add(db_user)
    # db.commit()
    # db.refresh(db_user)
    return {"message": "TBI"}


def add_new_game(db: Session, game: schemas.StartGame, username: str):
    logger.info("Adding new game")
    try:
        game_db = games.get_game_by_name(db, game.game)
        user = get_user(db, username)
        user_game = models.UsersGames(
            user=user.name,
            user_id=user.id,
            game=game.game,
            game_id=game_db.id,
            platform=game.platform,
            started_date=datetime.datetime.now(),
        )
        db.add(user_game)
        db.commit()
    except Exception as e:
        logger.info(e)
    return {"message": "Game added to user list"}


def update_game(db: Session, game_name, player, score, platform, seconds):
    try:
        stmt = (
            update(models.UsersGames)
            .where(
                models.UsersGames.game == game_name,
                models.UsersGames.player == player,
            )
            .values(
                game=game_name,
                player=player,
                platform=platform,
                score=score,
                played_time=seconds,
                # last_update=str(datetime.datetime.now()),
            )
        )
        db.execute(stmt)
        db.commit()
        # session.close()
    except Exception as e:
        logger.info(e)


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
    return


def get_total_played_time(db: Session):
    stmt = select(
        models.TimeEntries.user, func.sum(models.TimeEntries.duration)
    ).group_by(models.TimeEntries.user)
    return db.execute(stmt)


def get_played_time_games(db: Session, user_id: str):
    stmt = (
        select(
            models.TimeEntries.project,
            func.sum(models.TimeEntries.duration),
        )
        .where(models.TimeEntries.user_id == user_id)
        .group_by(models.TimeEntries.project)
    )
    return db.execute(stmt)


# def user_played_time(db: Session):
#     stmt = select(
#         models.UsersGames.player, func.sum(models.UsersGames.played_time)
#     ).group_by(models.UsersGames.player)
#     result = db.execute(stmt)
#     return result


def get_games(db: Session, user_id) -> list[models.UsersGames]:
    return db.query(models.UsersGames).filter_by(user_id=user_id)


def get_game(db: Session, user_id, game) -> models.UsersGames:
    # stmt = (
    #         select(models.UsersGames.id)
    #         .where(UsersGames.player == player)
    #         .order_by(desc(UsersGames.row))
    #     )
    #     return session.execute(stmt).first()
    return db.query(models.UsersGames.id).filter_by(user_id=user_id, game=game).first()


def update_played_days(db: Session, player, played_days):
    try:
        stmt = (
            update(models.User)
            .where(models.User.name == player)
            .values(played_days=played_days)
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


def completed_games(db: Session, player):
    try:
        return (
            db.query(models.UsersGames)
            .filter_by(player=player, completed=1)
            .order_by(desc(models.UsersGames.completed_date))
        )
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


def streak(db: Session, player):
    try:
        return db.query(
            models.User.current_streak,
            models.User.best_streak,
            models.User.best_streak_date,
        ).filter_by(name=player)
    except Exception as e:
        logger.info(e)
        raise e


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
