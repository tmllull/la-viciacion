import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ..database import models, schemas
from ..utils import actions
from ..utils import actions as actions
from ..utils import logger
from ..utils import my_utils as utils
from ..utils.clockify_api import ClockifyApi

clockify = ClockifyApi()

#################
##### GAMES #####
#################


def get_games(db: Session, limit: int = None) -> list[models.GamesInfo]:
    return db.query(models.GamesInfo).limit(limit)


def get_game_by_name(db: Session, name: str) -> list[models.GamesInfo]:
    logger.info("Searching game by name: " + name)
    search = "%{}%".format(name)
    return db.query(models.GamesInfo).filter(models.GamesInfo.name.like(search))


def get_game_by_id(db: Session, game_id: int) -> models.GamesInfo:
    logger.info("Searching game by id: " + str(game_id))
    return db.query(models.GamesInfo).filter(models.GamesInfo.id == game_id).first()


def get_game_by_clockify_id(db: Session, id: str) -> models.GamesInfo:
    # logger.info("Searching game by clockify id: " + str(id))
    return db.query(models.GamesInfo).filter(models.GamesInfo.clockify_id == id).first()


async def new_game(db: Session, game: schemas.NewGame) -> models.GamesInfo:
    logger.info("Adding new game to DB: " + game.name)
    if game.clockify_id is None or game.clockify_id == "string":
        logger.info("No clockify ID. Adding to clockify...")
        clockify_id = clockify.add_project(game.name)["id"]
        new_game = {"name": game.name, "id": clockify_id}
        game_info = await utils.get_new_game_info(new_game)
        # logger.info(game_info)
        game = models.GamesInfo(
            name=game_info.name,
            dev=game_info.dev,
            steam_id=game_info.steam_id,
            image_url=game_info.image_url,
            release_date=game_info.release_date,
            clockify_id=clockify_id,
            genres=game_info.genres,
            avg_time=game_info.avg_time,
            current_ranking=1000000000,
        )
    else:
        game = models.GamesInfo(
            name=game.name,
            dev=game.dev,
            steam_id=game.steam_id,
            image_url=game.image_url,
            release_date=game.release_date,
            clockify_id=game.clockify_id,
            genres=game.genres,
            avg_time=game.avg_time,
            current_ranking=1000000000,
        )
    try:
        db.add(game)
        db.commit()
        db.refresh(game)
        return game
    except Exception as e:
        if "Duplicate" in str(e):
            db.rollback()
        else:
            logger.info("Error adding new game: " + str(e))
            raise e


def get_all_played_games(db: Session):
    stmt = select(models.TimeEntries.project, models.TimeEntries.project_id)
    return db.execute(stmt)


def update_avg_time_game(db: Session, game_id: str, avg_time: int):
    try:
        stmt = (
            update(models.GamesInfo)
            .where(models.GamesInfo.id == game_id)
            .values(
                avg_time=avg_time,
            )
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
        raise e


def update_game(db: Session, game: models.GamesInfo):
    try:
        stmt = (
            update(models.GamesInfo)
            .where(models.GamesInfo.name == game)
            .values(
                game=game.name,
                dev=game.dev,
                steam_id=game.steam_id,
                image_url=game.image_url,
                release_date=game.release_date,
                clockify_id=game.clockify_id,
                genres=game.genres,
                avg_time=game.avg_time,
            )
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
        raise e


def update_total_played_time(db: Session, clockify_id, total_played):
    try:
        stmt = (
            update(models.GamesInfo)
            .where(models.GamesInfo.clockify_id == clockify_id)
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


def get_most_played_time(db: Session, limit: int = None) -> list[models.GamesInfo]:
    if limit is not None:
        return (
            db.query(models.GamesInfo)
            .order_by(desc(models.GamesInfo.played_time))
            .limit(limit)
        )
    else:
        return db.query(models.GamesInfo).order_by(desc(models.GamesInfo.played_time))


def current_ranking_hours(db: Session, limit: int = 11) -> list[models.GamesInfo]:
    try:
        return (
            db.query(models.GamesInfo)
            .order_by(asc(models.GamesInfo.current_ranking))
            .limit(limit)
        )
    except Exception as e:
        logger.info(e)


def update_current_ranking_hours(db: Session, i, game):
    try:
        stmt = (
            update(models.GamesInfo)
            .where(models.GamesInfo.name == game)
            .values(current_ranking=i)
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
