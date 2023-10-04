import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ...utils import actions
from ...utils import actions as actions
from ...utils import logger
from ...utils import my_utils as utils
from ...utils.clockify_api import ClockifyApi
from .. import models, schemas

clockify = ClockifyApi()

#################
##### GAMES #####
#################


def get_games(db: Session, skip: int = 0, limit: int = 100) -> list[models.GamesInfo]:
    return db.query(models.GamesInfo).offset(skip).limit(limit).all()


def get_game_by_name(db: Session, name: str) -> models.GamesInfo:
    logger.info("Searching game: " + name)
    return db.query(models.GamesInfo).filter(models.GamesInfo.name == name).first()


def game_exists(db: Session, game_name: str):
    stmt = select(models.GamesInfo).where(models.GamesInfo.name == game_name)
    game = db.execute(stmt).first()
    if game:
        return True
    return False


# def new_game_by_name(db: Session, game: str):
#     return


def new_game(db: Session, game: schemas.NewGame):
    try:
        game = models.GamesInfo(
            name=game.name,
            dev=game.dev,
            steam_id=game.steam_id,
            image_url=game.image_url,
            release_date=game.release_date,
            clockify_id=game.clockify_id,
            genres=game.genres,
            avg_time=game.avg_time,
            last_ranking=1000000000,
            current_ranking=1000000000,
        )
        db.add(game)
        db.commit()
        db.refresh(game)
        return game
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            db.rollback()
        else:
            logger.info("Error adding new game: " + str(e))
            raise e


# def add_new_game(
#     db: Session,
#     game,
#     dev=None,
#     steam_id=None,
#     released=None,
#     genres=None,
#     avg_time=None,
#     clockify_id=None,
#     image_url=None,
# ):
#     try:
#         game = models.GamesInfo(
#             game=game,
#             dev=dev,
#             steam_id=steam_id,
#             image_url=image_url,
#             release_date=released,
#             clockify_id=clockify_id,
#             genres=genres,
#             avg_time=avg_time,
#             last_ranking=1000000000,
#             current_ranking=1000000000,
#         )
#         db.add(game)
#         db.commit()
#         db.refresh(game)
#     except Exception as e:
#         if "UNIQUE constraint failed" in str(e):
#             db.rollback()
#         else:
#             logger.info("Error adding new game: " + str(e))
#             raise e


def get_all_played_games(db: Session):
    stmt = select(models.TimeEntries.project, models.TimeEntries.project_id)
    return db.execute(stmt)


def update_game(
    db: Session,
    game,
    dev=None,
    steam_id=None,
    released=None,
    genres=None,
    avg_time=None,
    clockify_id=None,
    image_url=None,
):
    try:
        stmt = (
            update(models.GamesInfo)
            .where(models.GamesInfo.name == game)
            .values(
                game=game,
                dev=dev,
                steam_id=steam_id,
                image_url=image_url,
                release_date=released,
                clockify_id=clockify_id,
                genres=genres,
                avg_time=avg_time,
            )
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
        raise e


def update_total_played_time(db: Session, game, total_played):
    try:
        stmt = (
            update(models.GamesInfo)
            .where(models.GamesInfo.name == game)
            .values(played_time=total_played)
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
        raise e


def game_avg_time(db: Session, game):
    stmt = select(models.GamesInfo.avg_time).where(models.GamesInfo.name == game)
    result = db.execute(stmt).first()
    return result


def total_played_time_by_game(db: Session, game):
    stmt = select(
        models.TimeEntries.project, func.sum(models.TimeEntries.duration)
    ).where(models.TimeEntries.project == game)
    result = db.execute(stmt)
    return result


def total_played_time_all(db: Session):
    stmt = select(
        models.TimeEntries.project, func.sum(models.TimeEntries.duration)
    ).group_by(models.TimeEntries.project)
    result = db.execute(stmt)
    return result


def most_played_time(db: Session):
    stmt = select(models.GamesInfo.name).order_by(desc(models.GamesInfo.played_time))
    result = db.execute(stmt)
    return result
