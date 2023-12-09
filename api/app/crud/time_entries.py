import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ..config import Config
from ..database import models, schemas
from ..utils import actions
from ..utils import actions as actions
from ..utils import logger
from ..utils import my_utils as utils
from ..utils.clockify_api import ClockifyApi
from . import clockify, games, users

clockify_api = ClockifyApi()
config = Config()


def get_users_played_time(db: Session):
    stmt = select(
        models.TimeEntry.user_id, func.sum(models.TimeEntry.duration)
    ).group_by(models.TimeEntry.user_id)
    return db.execute(stmt)


def get_user_played_time(db: Session, user_id: str):
    stmt = (
        select(
            models.TimeEntry.user_id,
            func.sum(models.TimeEntry.duration),
        )
        .where(models.TimeEntry.user_id == user_id)
        .group_by(models.TimeEntry.user_id)
    )
    return db.execute(stmt).first()


def get_games_played_time(db: Session):
    stmt = select(
        models.TimeEntry.project_clockify_id, func.sum(models.TimeEntry.duration)
    ).group_by(models.TimeEntry.project_clockify_id)
    result = db.execute(stmt)
    return result


# def get_game_played_time(db: Session, game):
#     stmt = select(models.TimeEntry.project_clockify_id, func.sum(models.TimeEntry.duration)).where(
#         models.TimeEntry.project == game
#     )
#     result = db.execute(stmt)
#     return result


def get_user_games_played_time(db: Session, user_id: str) -> list[models.TimeEntry]:
    stmt = (
        select(
            models.TimeEntry.project_clockify_id,
            func.sum(models.TimeEntry.duration),
        )
        .where(models.TimeEntry.user_id == user_id)
        .group_by(models.TimeEntry.project_clockify_id)
    )
    return db.execute(stmt)


def get_time_entries(db: Session, start_date: str = None) -> list[models.TimeEntry]:
    if start_date is None:
        return db.query(models.TimeEntry).order_by(models.TimeEntry.user_id)
    else:
        logger.info(start_date)
        return (
            db.query(models.TimeEntry)
            .filter(models.TimeEntry.start >= start_date)
            .order_by(models.TimeEntry.user_id)
        )


def get_played_days(
    db: Session, user_id: int, start_date: str = None, end_date: str = None
) -> list:
    played_days = []
    if start_date is None:
        start_date = "2000-01-01"
    if end_date is None:
        end_date = "3000-12-31"
    played_start_days = (
        db.query(func.DATE(models.TimeEntry.start))
        .filter(models.TimeEntry.user_id == user_id)
        .filter(func.DATE(models.TimeEntry.start) >= start_date)
        .filter(func.DATE(models.TimeEntry.end) >= start_date)
        .filter(func.DATE(models.TimeEntry.start) <= end_date)
        .filter(func.DATE(models.TimeEntry.end) <= end_date)
        .distinct()
        .all()
    )
    for played_day in played_start_days:
        played_days.append(played_day[0])
    return sorted(played_days)


async def sync_clockify_entries_db(db: Session, user: models.User, entries):
    for entry in entries:
        if entry["projectId"] is None:
            continue
        try:
            start = entry["timeInterval"]["start"]
            end = entry["timeInterval"]["end"]
            duration = entry["timeInterval"]["duration"]
            platform = None
            if entry["tagIds"] is not None and len(entry["tagIds"]) > 0:
                platform = entry["tagIds"][0]
                # Revise the following code if needed
                # platform = clockify.get_tag_by_id(db, entry["tagIds"][0])
                # if platform is not None:
                #     platform = platform[0]
            start = utils.change_timezone_clockify(start)
            if end is not None and end != "":
                end = utils.change_timezone_clockify(end)
            else:
                end = None
            # Check if game on clockify already exists on local DB
            game = games.get_game_by_clockify_id(db, entry["projectId"])
            if game is not None:
                game_name = game.name
                game_id = game.id
            else:
                project = clockify_api.get_project_by_id(entry["projectId"])
                game_name = project["name"]
                new_game_info = await utils.get_new_game_info(project)
                new_game = await games.new_game(db, new_game_info)
                game_id = new_game.id
            # Add game to GameStatistics (if needed)
            games.create_game_statistics(db, game_id)
            # Check if player already plays the game
            # logger.info("Checkpoint 4")
            already_playing = users.get_game_by_id(db, user.id, game_id)
            # logger.info("Checkpoint 5")
            if not already_playing:
                logger.info(
                    "USER NOT PLAYING GAME: " + game_name + " - " + str(game_id)
                )
                new_user_game = schemas.NewGameUser(
                    project_clockify_id=entry["projectId"], platform=platform
                )
                users.add_new_game(db, new_user_game, user, start)
                already_playing = users.get_game_by_id(db, user.id, game_id)
            # TODO: revise if this else is needed and how to implement it properly
            elif platform is not None and already_playing.platform != platform:
                stmt = (
                    update(models.UserGame)
                    .where(models.UserGame.id == already_playing.id)
                    .values(
                        platform=platform,
                    )
                )
                db.execute(stmt)
                db.commit()
            stmt = select(models.TimeEntry).where(models.TimeEntry.id == entry["id"])
            # Check if time entry already exists (to update it if needed)
            exists = db.execute(stmt).first()
            if not exists:
                if end is not None:
                    new_entry = models.TimeEntry(
                        id=entry["id"],
                        user_id=user.id,
                        user_clockify_id=user.clockify_id,
                        project_clockify_id=entry["projectId"],
                        start=start,
                        end=end,
                        duration=utils.convert_clockify_duration(duration),
                    )
                else:
                    new_entry = models.TimeEntry(
                        id=entry["id"],
                        user_id=user.id,
                        user_clockify_id=user.clockify_id,
                        project_clockify_id=entry["projectId"],
                        start=start,
                    )
                db.add(new_entry)
            else:
                if end is not None:
                    stmt = (
                        update(models.TimeEntry)
                        .where(models.TimeEntry.id == entry["id"])
                        .values(
                            project_clockify_id=entry["projectId"],
                            start=start,
                            end=end,
                            duration=utils.convert_clockify_duration(duration),
                        )
                    )
                else:
                    stmt = (
                        update(models.TimeEntry)
                        .where(models.TimeEntry.id == entry["id"])
                        .values(
                            project_clockify_id=entry["projectId"],
                            start=start,
                        )
                    )
                db.execute(stmt)
                update_game = models.UserGame(platform=platform)
                users.update_game(db, update_game, already_playing.id)
            db.commit()
            # TODO: Check time achievements related to session
            if end is not None:
                pass
        except Exception as e:
            db.rollback()
            logger.info("Error adding time entry " + str(entry) + ": " + str(e))
            raise e
    # return


# def get_all_played_games(db: Session):
#     stmt = select(models.TimeEntry.project, models.TimeEntry.project_id)
#     return db.execute(stmt)
