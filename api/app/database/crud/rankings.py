import datetime
from typing import Union

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ...utils import actions as actions
from ...utils import logger
from ...utils import my_utils as utils
from ...utils.clockify_api import ClockifyApi
from .. import models, schemas

clockify = ClockifyApi()

####################
##### RANKINGS #####
####################


def update_current_ranking_hours_game(db: Session, i, game):
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


def update_last_ranking_hours_game(db: Session, i, game):
    try:
        stmt = (
            update(models.GamesInfo)
            .where(models.GamesInfo.name == game)
            .values(last_ranking=i)
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)


def get_current_ranking_games(db: Session, limit: int = 11):
    try:
        stmt = (
            select(models.GamesInfo.name)
            .order_by(asc(models.GamesInfo.current_ranking))
            .limit(limit)
        )
        return db.execute(stmt)
    except Exception as e:
        logger.info(e)


def get_current_ranking_hours_players(db: Session):
    try:
        stmt = select(models.User.name, models.User.current_ranking_hours).order_by(
            asc(models.User.current_ranking_hours)
        )
        return db.execute(stmt)
    except Exception as e:
        logger.info(e)


def get_last_ranking_hours_players(db: Session):
    try:
        stmt = select(models.User.name, models.User.last_ranking_hours).order_by(
            asc(models.User.last_ranking_hours)
        )
        return db.execute(stmt)
    except Exception as e:
        logger.info(e)


def get_last_ranking_games(db: Session, limit: int = 11):
    try:
        stmt = (
            select(models.GamesInfo.name)
            .order_by(asc(models.GamesInfo.last_ranking))
            .limit(limit)
        )
        return db.execute(stmt)
    except Exception as e:
        logger.info(e)


def update_current_ranking_hours_user(db: Session, ranking, user):
    stmt = (
        update(models.User)
        .where(models.User.name == user)
        .values(current_ranking_hours=ranking)
    )
    db.execute(stmt)
    db.commit()


def update_last_ranking_hours_user(db: Session, ranking, user):
    stmt = (
        update(models.User)
        .where(models.User.name == user)
        .values(last_ranking_hours=ranking)
    )
    db.execute(stmt)
    db.commit()


def get_ranking_games(db: Session):
    try:
        stmt = select(
            models.GamesInfo.name,
            models.GamesInfo.played_time,
            models.GamesInfo.last_ranking,
            models.GamesInfo.current_ranking,
        ).order_by(desc(models.GamesInfo.played_time))
        return db.execute(stmt)
    except Exception as e:
        logger.info(e)
        raise e


def ranking_days(db: Session):
    try:
        return db.query(models.User.name, models.User.played_days).order_by(
            desc(models.User.played_days)
        )
    except Exception as e:
        logger.info(e)
        raise e


def ranking_streak(db: Session):
    try:
        return db.query(models.User.name, models.User.best_streak).order_by(
            desc(models.User.best_streak)
        )
    except Exception as e:
        logger.info(e)
        raise e


def ranking_current_streak(db: Session):
    try:
        return db.query(models.User.name, models.User.current_streak).order_by(
            desc(models.User.current_streak)
        )
    except Exception as e:
        logger.info(e)
        raise e


def ranking_achievements(db: Session):
    return (
        db.query(
            models.UserAchievements.player, func.count(models.UserAchievements.player)
        )
        .group_by(models.UserAchievements.player)
        .order_by(func.count(models.UserAchievements.player).desc())
        .all()
    )


def ranking_num_games(db: Session):
    result = (
        db.query(models.UsersGames.player, func.count(models.UsersGames.game))
        .group_by(models.UsersGames.player)
        .order_by(func.count(models.UsersGames.game).desc())
        .all()
    )
    return result


def ranking_completed_games(db: Session):
    return (
        db.query(models.UsersGames.player, func.count(models.UsersGames.game))
        .group_by(models.UsersGames.player)
        .filter_by(completed=1)
        .order_by(func.count(models.UsersGames.game).desc())
        .all()
    )


def ranking_last_played_games(db: Session):
    # try:
    #     stmt = (
    #         select(models.GamesInfo.name)
    #         .order_by(asc(models.GamesInfo.current_ranking))
    #         .limit(limit)
    #     )

    #     return db.execute(stmt)
    # except Exception as e:
    #     logger.info(e)
    stmt = select(
        models.TimeEntries.project, models.TimeEntries.user, models.TimeEntries.start
    ).order_by(desc(models.TimeEntries.start))
    return db.execute(stmt).fetchall()


def ranking_most_played_games(db: Session, limit: int = 10):
    stmt = (
        select(models.GamesInfo.name, models.GamesInfo.played_time)
        .order_by(desc(models.GamesInfo.played_time))
        .limit(limit)
    )
    return db.execute(stmt).fetchall()
