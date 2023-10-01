import datetime

from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ..utils import actions as utils
from ..utils import logger
from ..utils.clockify_api import ClockifyApi
from . import models, schemas

clockify = ClockifyApi()

#################
##### USERS #####
#################


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_id(db: Session, id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_tg_username(db: Session, telegram_username: str = None):
    return (
        db.query(models.User)
        .filter(models.User.telegram_username == telegram_username)
        .first()
    )


def get_user_by_tg_id(db: Session, telegram_id: int = None):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_or_update_game_user(db: Session, game_name, player, score, platform, seconds):
    try:
        stmt = select(models.UsersGames).where(
            models.UsersGames.game == game_name, models.UsersGames.player == player
        )
        game = db.execute(stmt).first()
        if not game:
            # logger.info(player + " has started new game: " + game_name)
            user_game = models.UsersGames(
                game=game_name,
                player=player,
                platform=platform,
                score=score,
                started_date=datetime.datetime.now().date(),
                played_time=seconds,
                last_update=str(datetime.datetime.now().timestamp()),
            )
            db.add(user_game)
            db.commit()
            return True
        else:
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
            return False
        # session.close()
    except Exception as e:
        logger.info(e)


def user_played_time(db: Session):
    stmt = select(
        models.UsersGames.player, func.sum(models.UsersGames.played_time)
    ).group_by(models.UsersGames.player)
    result = db.execute(stmt)
    return result


def user_played_games(db: Session, player):
    return (
        db.query(
            models.UsersGames.game,
            models.UsersGames.platform,
            models.UsersGames.row,
            models.UsersGames.played_time,
        )
        .filter_by(player=player)
        .order_by(desc(models.UsersGames.last_update))
    )


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


def my_top_games(db: Session, player, limit: int = 10):
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


def my_completed_games(db: Session, player):
    try:
        return db.query(models.UsersGames).filter_by(player=player, completed=1)
    except Exception as e:
        logger.info(e)
        raise e


def my_last_completed_games(db: Session, player):
    try:
        return (
            db.query(models.UsersGames.game)
            .filter_by(player=player, completed=1)
            .order_by(desc(models.UsersGames.last_update))
        )
    except Exception as e:
        logger.info(e)
        raise e


def my_achievements(db: Session, player):
    try:
        stmt = select(models.UserAchievements.achievement).where(
            models.UserAchievements.player == player
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e


def my_streak(db: Session, player):
    try:
        return db.query(
            models.User.current_streak,
            models.User.best_streak,
            models.User.best_streak_date,
        ).filter_by(name=player)
    except Exception as e:
        logger.info(e)
        raise e


def set_user_achievement(db: Session, player, achievement):
    try:
        ach = models.UserAchievements(player=player, achievement=achievement)
        db.add(ach)
        db.commit()
        return False
    except Exception as e:
        db.rollback()
        if "Duplicate entry" in str(e) or "UNIQUE" in str(e):
            # logger.info("Logro '" + achievement + "' ya desbloqueado")
            return True
        else:
            raise Exception("Error checking achievement:", e)


#################
##### GAMES #####
#################


def game_exists(db: Session, game_name: str):
    stmt = select(models.GamesInfo).where(models.GamesInfo.game == game_name)
    game = db.execute(stmt).first()
    if game:
        return True
    return False


def add_new_game(
    db: Session,
    game,
    dev=None,
    steam_id=None,
    released=None,
    genres=None,
    mean_time=None,
    clockify_id=None,
    image_url=None,
):
    try:
        game = models.GamesInfo(
            game=game,
            dev=dev,
            steam_id=steam_id,
            image_url=image_url,
            release_date=released,
            clockify_id=clockify_id,
            genres=genres,
            mean_time=mean_time,
            last_ranking=1000,
            current_ranking=1000,
        )
        db.add(game)
        db.commit()
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            db.rollback()
        else:
            logger.info("Error adding new game: " + str(e))
            raise e


def update_game(
    db: Session,
    game,
    dev=None,
    steam_id=None,
    released=None,
    genres=None,
    mean_time=None,
    clockify_id=None,
    image_url=None,
):
    try:
        stmt = (
            update(models.GamesInfo)
            .where(models.GamesInfo.game == game)
            .values(
                game=game,
                dev=dev,
                steam_id=steam_id,
                image_url=image_url,
                release_date=released,
                clockify_id=clockify_id,
                genres=genres,
                mean_time=mean_time,
            )
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
        raise e


def update_total_played_game(db: Session, game, total_played):
    try:
        stmt = (
            update(models.GamesInfo)
            .where(models.GamesInfo.game == game)
            .values(played_time=total_played)
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)
        raise e


def game_completed(db: Session, player, game):
    stmt = select(models.UsersGames).where(
        models.UsersGames.game == game,
        models.UsersGames.player == player,
        models.UsersGames.completed == 1,
    )
    game = db.execute(stmt).first()
    if game:
        return True
    return False


def complete_game(db: Session, player, game_name, score, time, seconds):
    try:
        stmt = (
            update(models.UsersGames)
            .where(
                models.UsersGames.game == game_name, models.UsersGames.player == player
            )
            .values(
                score=score,
                played_time=seconds,
                completed=1,
                completed_date=datetime.datetime.now().date(),
            )
        )
        db.execute(stmt)
        db.commit()

        completed_games_count = (
            db.query(models.UsersGames).filter_by(player=player, completed=1).count()
        )

        return completed_games_count
    except Exception as e:
        db.rollback()
        if "Duplicate entry" in str(e) or "UNIQUE" in str(e):
            # logger.info("Logro '" + achievement + "' ya desbloqueado")
            return False
        else:
            raise Exception("Error checking achievement:", e)


def mean_time_game(db: Session, game):
    stmt = select(models.GamesInfo.mean_time).where(models.GamesInfo.game == game)
    result = db.execute(stmt).first()
    return result


def total_played_time_games(db: Session):
    stmt = select(
        models.UsersGames.game, func.sum(models.UsersGames.played_time)
    ).group_by(models.UsersGames.game)
    result = db.execute(stmt)
    return result


####################
##### RANKINGS #####
####################


def update_current_ranking_hours_game(db: Session, i, game):
    try:
        stmt = (
            update(models.GamesInfo)
            .where(models.GamesInfo.game == game)
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
            .where(models.GamesInfo.game == game)
            .values(last_ranking=i)
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logger.info(e)


def get_current_ranking_games(db: Session, limit: int = 11):
    try:
        stmt = (
            select(models.GamesInfo.game)
            .order_by(asc(models.GamesInfo.current_ranking))
            .limit(limit)
        )
        return db.execute(stmt)
    except Exception as e:
        logger.info(e)


def get_current_ranking_players(db: Session):
    try:
        stmt = select(models.User.name, models.User.current_ranking_hours).order_by(
            asc(models.User.current_ranking_hours)
        )
        return db.execute(stmt)
    except Exception as e:
        logger.info(e)


def get_last_ranking_games(db: Session, limit: int = 11):
    try:
        stmt = (
            select(models.GamesInfo.game)
            .order_by(asc(models.GamesInfo.last_ranking))
            .limit(limit)
        )
        return db.execute(stmt)
    except Exception as e:
        logger.info(e)


def get_last_ranking_players(db: Session):
    try:
        stmt = select(models.User.name, models.User.last_ranking_hours).order_by(
            asc(models.User.last_ranking_hours)
        )
        return db.execute(stmt)
    except Exception as e:
        logger.info(e)


def update_current_ranking_hours(db: Session, ranking, player):
    stmt = (
        update(models.User)
        .where(models.User.name == player)
        .values(current_ranking_hours=ranking)
    )
    db.execute(stmt)
    db.commit()


def update_last_ranking_hours(db: Session, ranking, player):
    stmt = (
        update(models.User)
        .where(models.User.name == player)
        .values(last_ranking_hours=ranking)
    )
    db.execute(stmt)
    db.commit()


def get_ranking_games(db: Session):
    try:
        stmt = select(
            models.GamesInfo.game,
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
    stmt = select(models.UsersGames.game, models.UsersGames.played_time).order_by(
        desc(models.UsersGames.last_update)
    )
    return db.execute(stmt).fetchall()


def ranking_most_played_games(db: Session, limit: int = 10):
    stmt = (
        select(models.GamesInfo.game, models.GamesInfo.played_time)
        .order_by(desc(models.GamesInfo.played_time))
        .limit(limit)
    )
    return db.execute(stmt).fetchall()


######################
#### ACHIEVEMENTS ####
######################


def get_achievements_list(db: Session):
    return db.query(
        models.Achievement.achievement,
    )


def lose_streak(db: Session, player, streak, date=None):
    if streak == 0:
        stmt = select(models.User.last_streak).where(models.User.name == player)
        last = db.execute(stmt).first()
        if last[0] != None and last[0] != 0:
            stmt = (
                update(models.User)
                .where(models.User.name == player)
                .values(last_streak=streak, last_streak_date=date)
            )
            db.execute(stmt)
            db.commit()
            return last
    stmt = (
        update(models.User)
        .where(models.User.name == player)
        .values(last_streak=streak, last_streak_date=date)
    )
    db.execute(stmt)
    db.commit()
    return False


def best_streak(db: Session, player, streak, date):
    stmt = select(models.User.best_streak).where(models.User.name == player)
    best_streak = db.execute(stmt).first()
    if best_streak is None or best_streak <= streak:
        stmt = (
            update(models.User)
            .where(models.User.name == player)
            .values(best_streak=streak, best_streak_date=date)
        )
        db.execute(stmt)
        db.commit()


def current_streak(db: Session, player, streak):
    stmt = (
        update(models.User)
        .where(models.User.name == player)
        .values(current_streak=streak)
    )
    db.execute(stmt)
    db.commit()


####################
##### Clockify #####
####################


def sync_clockify_entries(db: Session, user_id, entries):
    user = get_user_by_id(db, id=user_id)
    logger.info("Sync entries for user " + str(user.name))
    for entry in entries:
        try:
            start = entry["timeInterval"]["start"]
            end = entry["timeInterval"]["end"]
            duration = entry["timeInterval"]["duration"]
            if end is None:
                end = ""
            if duration is None:
                duration = ""
            project_name = clockify.get_project(entry["projectId"])["name"]
            stmt = select(models.TimeEntries).where(
                models.TimeEntries.id == entry["id"]
            )
            exists = db.execute(stmt).first()
            if not exists:
                new_entry = models.TimeEntries(
                    id=entry["id"],
                    user=user.name,
                    user_id=user.id,
                    user_clockify_id=user.clockify_id,
                    project=project_name,
                    project_id=entry["projectId"],
                    start=start,
                    end=end,
                    duration=utils.convert_clockify_duration(duration),
                )
                db.add(new_entry)
            else:
                stmt = (
                    update(models.TimeEntries)
                    .where(models.TimeEntries.id == entry["id"])
                    .values(
                        user_clockify_id=user.clockify_id,
                        user=user.name,
                        user_id=user.id,
                        project=project_name,
                        project_id=entry["projectId"],
                        start=start,
                        end=end,
                        duration=utils.convert_clockify_duration(duration),
                    )
                )
                db.execute(stmt)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.info("Error adding new entry " + str(entry) + ": " + str(e))
            raise e
        # logger.info(entry["id"])
        # exit()
    return


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
