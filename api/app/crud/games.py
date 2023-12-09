import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..database import models, schemas
from ..utils import actions
from ..utils import actions as actions
from ..utils import logger
from ..utils import my_utils as utils
from ..utils.clockify_api import ClockifyApi

clockify_api = ClockifyApi()

#################
##### GAMES #####
#################


def get_games(db: Session, limit: int = None) -> list[models.Game]:
    return db.query(models.Game).limit(limit)


def get_game_by_name(db: Session, name: str) -> list[models.Game]:
    logger.info("Searching game by name: " + name)
    search = "%{}%".format(name)
    return db.query(models.Game).filter(models.Game.name.like(search))


def get_game_by_id(db: Session, game_id: int) -> models.Game:
    # logger.info("Searching game by id: " + str(game_id))
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def get_game_by_clockify_id(db: Session, id: str) -> models.Game:
    # logger.info("Searching game by clockify id: " + str(id))
    return db.query(models.Game).filter(models.Game.clockify_id == id).first()


async def new_game(db: Session, game: schemas.NewGame) -> models.Game:
    logger.info("Adding new game to DB: " + game.name)
    # game_info = await utils.get_new_game_info(game.name)
    if game.clockify_id is None or not utils.check_hex(game.clockify_id):
        logger.info("No clockify ID. Adding to clockify...")
        clockify_id = clockify_api.add_project(game.name)["id"]
        new_game = {"name": game.name, "id": clockify_id}
        game_info = await utils.get_new_game_info(new_game)
        game_to_add = models.Game(
            name=game_info.name,
            dev=game_info.dev,
            steam_id=game_info.steam_id,
            image_url=game_info.image_url,
            release_date=game_info.release_date,
            clockify_id=clockify_id,
            genres=game_info.genres,
            avg_time=game_info.avg_time,
            # current_ranking=1000000000,
        )
    else:
        game_to_add = models.Game(
            name=game.name,
            dev=game.dev,
            steam_id=game.steam_id,
            image_url=game.image_url,
            release_date=game.release_date,
            clockify_id=game.clockify_id,
            genres=game.genres,
            avg_time=game.avg_time,
            # current_ranking=1000000000,
        )
    try:
        db.add(game_to_add)
        db.commit()
        db.refresh(game_to_add)
        game_added = game_to_add
        try:
            game_statistics = models.GameStatistics(
                game_id=game_added.id, current_ranking=100000000
            )
            db.add(game_statistics)
            db.commit()
            # db.refresh(game_statistics)
        except Exception as e:
            db.rollback()
            if "Duplicate" not in str(e):
                # else:
                logger.info("Error adding new game statistics: " + str(e))
                raise e
        return game_added
    except Exception as e:
        db.rollback()
        if "Duplicate" not in str(e):
            # db.rollback()
            # else:
            logger.info("Error adding new game: " + str(e))
            raise e


def create_game_statistics(db: Session, game_id: int):
    try:
        game_statistics = models.GameStatistics(
            game_id=game_id, current_ranking=1000000
        )
        db.add(game_statistics)
        db.commit()
        db.refresh(game_statistics)

    except SQLAlchemyError as e:
        db.rollback()
        if "Duplicate" not in str(e):
            logger.info("Error creating user statistics: " + str(e))
            raise e


# def get_all_played_games(db: Session):
#     stmt = select(models.TimeEntries.project, models.TimeEntries.project_id)
#     return db.execute(stmt)


def update_avg_time_game(db: Session, game_id: str, avg_time: int):
    try:
        stmt = (
            update(models.Game)
            .where(models.Game.id == game_id)
            .values(
                avg_time=avg_time,
            )
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
        raise e


def update_game(db: Session, game_id: int, game: schemas.UpdateGame):
    try:
        db_game = get_game_by_id(db, game_id)
        name = game.name if game.name is not None else db_game.name
        dev = game.dev if game.dev is not None else db_game.dev
        steam_id = game.steam_id if game.steam_id is not None else db_game.steam_id
        image_url = game.image_url if game.image_url is not None else db_game.image_url
        release_date = (
            game.release_date if game.release_date is not None else db_game.release_date
        )
        clockify_id = (
            game.clockify_id if game.clockify_id is not None else db_game.clockify_id
        )
        genres = game.genres if game.genres is not None else db_game.genres
        avg_time = game.avg_time if game.avg_time is not None else db_game.avg_time
        stmt = (
            update(models.Game)
            .where(models.Game.id == game_id)
            .values(
                name=name,
                dev=dev,
                steam_id=steam_id,
                image_url=image_url,
                release_date=release_date,
                clockify_id=clockify_id,
                genres=genres,
                avg_time=avg_time,
            )
        )
        db.execute(stmt)
        db.commit()
        if clockify_id is not None:
            clockify_api.update_project_name(clockify_id, name)
        return db.query(models.Game).filter(models.Game.id == game_id).first()
    except Exception as e:
        db.rollback()
        logger.info("Error updating game: " + str(e))
        raise ("Error updating game: " + str(e))


def update_total_played_time(db: Session, clockify_id, total_played):
    try:
        game = get_game_by_clockify_id(db, clockify_id)
        stmt = (
            update(models.GameStatistics)
            .where(models.GameStatistics.game_id == game.id)
            .values(played_time=total_played)
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
        raise e


# def game_avg_time(db: Session, game):
#     stmt = select(models.GameStatistics.avg_time).where(models.GameStatistics.name == game)
#     result = db.execute(stmt).first()
#     return result


def get_most_played_time(db: Session, limit: int = None) -> list[models.GameStatistics]:
    if limit is not None:
        return (
            db.query(models.GameStatistics)
            .order_by(desc(models.GameStatistics.played_time))
            .limit(limit)
        )
    else:
        return db.query(models.GameStatistics).order_by(
            desc(models.GameStatistics.played_time)
        )


def current_ranking_hours(db: Session, limit: int = 11) -> list[models.GameStatistics]:
    try:
        return (
            db.query(models.GameStatistics)
            .order_by(asc(models.GameStatistics.current_ranking))
            .limit(limit)
        )
    except Exception as e:
        logger.info(e)


def update_current_ranking_hours(db: Session, i, game_id):
    try:
        # game_db = get_game_by_name(db, game)
        stmt = (
            update(models.GameStatistics)
            .where(models.GameStatistics.game_id == game_id)
            .values(current_ranking=i)
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(
            "Error updating current ranking for game " + str(game_id) + ". " + str(e)
        )
