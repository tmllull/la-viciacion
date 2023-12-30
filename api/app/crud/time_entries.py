import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, or_, select, text, update
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


def get_time_entry_by_date(
    db: Session, user_id: int, date: str, mode: int
) -> list[models.TimeEntry]:
    """_summary_

    Args:
        db (Session): _description_
        user_id (int): _description_
        date (str): _description_
        mode (int): 1==, 2<=, 3>=

    Returns:
        _type_: _description_
    """
    if mode == 1:
        return db.query(models.TimeEntry).filter(
            models.TimeEntry.user_id == user_id,
            or_(
                func.DATE(models.TimeEntry.start) == date,
                func.DATE(models.TimeEntry.end) == date,
            ),
        )
    elif mode == 2:
        return db.query(models.TimeEntry).filter(
            models.TimeEntry.user_id == user_id,
            or_(
                func.DATE(models.TimeEntry.start) <= date,
                func.DATE(models.TimeEntry.end) <= date,
            ),
        )
    elif mode == 3:
        return db.query(models.TimeEntry).filter(
            models.TimeEntry.user_id == user_id,
            or_(
                func.DATE(models.TimeEntry.start) >= date,
                func.DATE(models.TimeEntry.end) >= date,
            ),
        )


# def get_game_played_time(db: Session, game):
#     stmt = select(models.TimeEntry.project_clockify_id, func.sum(models.TimeEntry.duration)).where(
#         models.TimeEntry.project == game
#     )
#     result = db.execute(stmt)
#     return result


def get_user_games_played_time(
    db: Session, user_id: str, game_id: str = None
) -> list[models.TimeEntry]:
    if game_id is not None:
        stmt = (
            select(
                models.TimeEntry.project_clockify_id,
                func.sum(models.TimeEntry.duration),
            )
            .where(
                models.TimeEntry.user_id == user_id,
                models.TimeEntry.project_clockify_id == game_id,
            )
            .group_by(models.TimeEntry.project_clockify_id)
        )
    else:
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
) -> list[models.TimeEntry]:
    played_days = []
    if start_date is None:
        current_date = datetime.datetime.now()
        start_date = str(current_date.year) + "-01-01"
    if end_date is None:
        end_date = "3000-12-31"
    played_start_days = (
        db.query(func.DATE(models.TimeEntry.start))
        .filter(models.TimeEntry.user_id == user_id)
        .filter(func.DATE(models.TimeEntry.start) >= start_date)
        .filter(func.DATE(models.TimeEntry.start) <= end_date)
        .distinct()
        .all()
    )
    played_end_days = (
        db.query(func.DATE(models.TimeEntry.end))
        .filter(models.TimeEntry.user_id == user_id)
        .filter(func.DATE(models.TimeEntry.end) >= start_date)
        .filter(func.DATE(models.TimeEntry.end) <= end_date)
        .distinct()
        .all()
    )
    for played_day in played_start_days:
        played_days.append(played_day[0])
    for played_day in played_end_days:
        played_days.append(played_day[0])
    unique_dates = list(set(played_days))
    return sorted(unique_dates)


async def sync_clockify_entries_db(
    db: Session, user: models.User, entries, silent: bool
):
    # current_year = datetime.datetime.now().year
    for entry in entries:
        if entry["projectId"] is None:
            continue
        try:
            # Extract data from time entry
            start = entry["timeInterval"]["start"]
            end = entry["timeInterval"]["end"]
            duration = entry["timeInterval"]["duration"]
            platform = None
            completed = None
            if entry["tagIds"] is not None and len(entry["tagIds"]) > 0:
                for tag in entry["tagIds"]:
                    platform_check = clockify.get_platform_by_tag_id(db, tag)
                    completed_check = clockify.check_completed_tag_by_id(db, tag)
                    if completed is None and completed_check is not None:
                        completed = 1
                    if platform is None and platform_check is not None:
                        platform = tag

            start = utils.change_timezone_clockify(start)
            if end is not None and end != "":
                end = utils.change_timezone_clockify(end)
            else:
                end = None

            # Check if time entry already exists (to update it if needed) for current season
            time_entry_year = datetime.datetime.strptime(
                start, "%Y-%m-%d %H:%M:%S"
            ).year
            if time_entry_year == config.CURRENT_SEASON:
                stmt = select(models.TimeEntry).where(
                    models.TimeEntry.id == entry["id"]
                )
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
                    db.commit()
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
                    db.commit()

            # Check if historical time entry already exists (to update it if needed)
            # if duration == 0:
            #     continue
            stmt = select(models.TimeEntryHistorical).where(
                models.TimeEntryHistorical.id == entry["id"]
            )
            exists = db.execute(stmt).first()
            if not exists:
                if end is not None:
                    new_entry = models.TimeEntryHistorical(
                        id=entry["id"],
                        user_id=user.id,
                        user_clockify_id=user.clockify_id,
                        project_clockify_id=entry["projectId"],
                        start=start,
                        end=end,
                        duration=utils.convert_clockify_duration(duration),
                    )
                else:
                    new_entry = models.TimeEntryHistorical(
                        id=entry["id"],
                        user_id=user.id,
                        user_clockify_id=user.clockify_id,
                        project_clockify_id=entry["projectId"],
                        start=start,
                    )
                db.add(new_entry)
                db.commit()
            else:  # time entry exists. Update it
                if end is not None:
                    stmt = (
                        update(models.TimeEntryHistorical)
                        .where(models.TimeEntryHistorical.id == entry["id"])
                        .values(
                            project_clockify_id=entry["projectId"],
                            start=start,
                            end=end,
                            duration=utils.convert_clockify_duration(duration),
                        )
                    )
                else:
                    stmt = (
                        update(models.TimeEntryHistorical)
                        .where(models.TimeEntryHistorical.id == entry["id"])
                        .values(
                            project_clockify_id=entry["projectId"],
                            start=start,
                        )
                    )
                db.execute(stmt)
                db.commit()
                # update_game = models.UserGame(platform=platform)
                # users.update_game(db, update_game, already_playing.id)

            # Check if game on clockify already exists on local DB
            game = games.get_game_by_id(db, entry["projectId"])
            if game is not None:
                game_name = game.name
                game_id = game.id
            else:
                logger.info("Project " + entry["projectId"] + " not in DB")
                project = clockify_api.get_project_by_id(entry["projectId"])
                game_name = project["name"]
                new_game_info = await utils.get_new_game_info(project)
                new_game = await games.new_game(db, new_game_info)
                game_id = new_game.id

            # Add game to GameStatistics (if needed)
            games.create_game_statistics(db, game_id)
            games.create_game_statistics_historical(db, game_id)

            # Check if player already plays the game
            already_playing = users.get_game_by_id(db, user.id, game_id)
            if not already_playing:
                logger.info("User not playing " + game_name)
                new_user_game = schemas.NewGameUser(game_id=game_id, platform=platform)
                await users.add_new_game(
                    db,
                    game=new_user_game,
                    user=user,
                    start_date=start,
                    silent=silent,
                    from_sync=True,
                )
                already_playing = users.get_game_by_id(db, user.id, game_id)
            # TODO: revise if this else is needed and how to implement it properly
            if platform is not None and already_playing.platform != platform:
                stmt = (
                    update(models.UserGame)
                    .where(models.UserGame.id == already_playing.id)
                    .values(
                        platform=platform,
                    )
                )
                db.execute(stmt)
                db.commit()
            if completed is not None and already_playing.completed != 1:
                logger.info("Completing game " + str(game.id) + "...")
                played_time = get_user_games_played_time(db, user.id, game.id)
                # The follow list only will have 1 item
                for played_game in played_time:
                    users.update_played_time_game(
                        db, user.id, played_game[0], played_game[1]
                    )
                await users.complete_game(
                    db,
                    user.id,
                    game.id,
                    completed_date=start,
                    silent=silent,
                    from_sync=True,
                )
            update_game = models.UserGame(platform=platform)
            users.update_game(db, update_game, already_playing.id)

            db.commit()
            # TODO: Check time achievements related to session
            # if "-01-01" in start:
            #     pass
        except Exception as e:
            db.rollback()
            logger.info("Error adding time entry " + str(entry) + ": " + str(e))
            raise e
    # return


def get_time_entry_by_time(
    db: Session, user_id: int, duration: int, mode: int
) -> models.TimeEntry:
    """_summary_

    Args:
        db (Session): _description_
        user_id (int): _description_
        duration (int): _description_
        mode (int): 1==, 2<=, 3>=

    Returns:
        _type_: _description_
    """
    if mode == 1:
        time_entry = (
            db.query(models.TimeEntry)
            .filter(
                models.TimeEntry.user_id == user_id,
                models.TimeEntry.duration == duration,
            )
            .first()
        )
    elif mode == 2:
        time_entry = (
            db.query(models.TimeEntry)
            .filter(
                models.TimeEntry.user_id == user_id,
                models.TimeEntry.duration <= duration,
            )
            .first()
        )
    elif mode == 3:
        time_entry = (
            db.query(models.TimeEntry)
            .filter(
                models.TimeEntry.user_id == user_id,
                models.TimeEntry.duration >= duration,
            )
            .first()
        )
    return time_entry


def get_played_time_by_day():
    return


# def get_all_played_games(db: Session):
#     stmt = select(models.TimeEntry.project, models.TimeEntry.project_id)
#     return db.execute(stmt)
