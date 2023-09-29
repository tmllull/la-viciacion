import datetime
import logging
import re
import sys
import uuid

import utils.logger as logger
from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import sessionmaker
from utils.achievements_list import AchievementsList
from utils.clockify_api import ClockifyApi
from utils.config import Config
from utils.db_schemas import *

config = Config()
clockify = ClockifyApi()

if config.DB_MODE == "mysql":
    # engine = create_engine(
    #     f"mysql+pymysql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}",
    #     connect_args={
    #         "ssl": {
    #             "ca": None,
    #         }
    #     },
    #     pool_size=20,
    # )
    # with engine.connect() as conn:
    #     conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}"))
    engine = create_engine(
        f"mysql+pymysql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}/{config.DB_NAME}",
        connect_args={
            "ssl": {
                "ca": None,
            }
        },
        pool_size=20,
    )
elif config.DB_MODE == "sqlite":
    engine = create_engine("sqlite:///db/" + config.DB_NAME + ".sqlite")
else:
    exit("Invalid DB_MODE")


class DatabaseConnector:
    def __init__(self, init=False, reset=False) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()
        with self.session.begin():
            if init:
                logger.info("Init DB")
                # Base.metadata.drop_all(engine)
                Base.metadata.drop_all(
                    engine,
                    tables=[
                        GamesInfo.__table__,
                        UsersGames.__table__,
                        UserAchievements.__table__,
                        Achievement.__table__,
                        # TimeEntries.__table__,
                    ],
                )
            if reset:
                logger.info("Reset DB")
                Base.metadata.drop_all(
                    engine,
                    tables=[
                        UsersGames.__table__,
                        UserAchievements.__table__,
                        Achievement.__table__,
                        # TimeEntries.__table__,
                    ],
                )
            Base.metadata.create_all(engine)
        self.set_achievements_list()

    ##################
    ###### INIT ######
    ##################

    def set_achievements_list(self):
        session = sessionmaker(bind=engine)()
        for item in vars(AchievementsList):
            if not item.startswith("__"):
                stmt = select(Achievement).where(Achievement.achievement == item)
                exists = session.execute(stmt).first()
                if not exists:
                    ach = Achievement(achievement=item)
                    session.add(ach)
        session.commit()

    #############################
    ####### BASIC METHODS #######
    #############################

    def get_users(self):
        """Get all users

        Returns:
            list: A list of users
        """
        try:
            logger.info("Getting user")
            session = sessionmaker(bind=engine)()
            stmt = select(
                User.telegram_username, User.name, User.telegram_id, User.clockify_id
            )
            return session.execute(stmt).fetchall()
        except Exception as e:
            logger.info(e)

    def get_user(self, telegram_id=None, telegram_username=None, name=None):
        """Check if user is allowed to use the bot. At least 1 param must be passed

        Args:
            telegram_id (int/string, optional): Telegram ID. Defaults to None.
            telegram_username (string, optional): Telegram username. Defaults to None.
            name (string, optional): User name. Defaults to None.

        Returns:
            Row: If user exists, return User info as SQL row. Else, returns None
        """
        session = sessionmaker(bind=engine)()
        if telegram_id is not None:
            stmt = select(User).where(User.telegram_id == telegram_id)
            user = session.execute(stmt).first()
            if user is None and telegram_username is not None:
                stmt = (
                    update(User)
                    .where(User.telegram_username == telegram_username)
                    .values(telegram_id=telegram_id)
                )
                session.execute(stmt)
                stmt = select(User).where(User.telegram_username == telegram_username)
                user = session.execute(stmt).first()
                session.commit()
                session.close()
            else:
                return None
        elif telegram_username is not None:
            stmt = select(User).where(User.telegram_username == telegram_username)
            user = session.execute(stmt).first()
            if user is None and telegram_id is not None:
                stmt = (
                    update(User)
                    .where(User.telegram_id == telegram_id)
                    .values(telegram_username=telegram_username)
                )
                session.execute(stmt)
                stmt = select(User).where(User.telegram_username == telegram_username)
                user = session.execute(stmt).first()
                session.commit()
                session.close()
            else:
                return False
            session.commit()
            session.close()
        elif name is not None:
            stmt = select(User).where(User.name == name)
            user = session.execute(stmt).first()
            session.commit()
            session.close()
        else:
            return False
        return user

    def convert_clockify_duration(self, duration):
        match = re.match(r"PT(\d+H)?(\d+M)?", duration)
        if match:
            horas_str = match.group(1)
            minutos_str = match.group(2)

            horas = int(horas_str[:-1]) if horas_str else 0
            minutos = int(minutos_str[:-1]) if minutos_str else 0

            # Convertir horas y minutos a segundos
            segundos = horas * 3600 + minutos * 60

            return segundos
        else:
            return 0

    def sync_clockify_entries(self, player, entries):
        user = self.get_user(name=player)
        session = sessionmaker(bind=engine)()
        for entry in entries:
            try:
                project_name = clockify.get_project(entry["projectId"])["name"]
                stmt = select(TimeEntries).where(TimeEntries.id == entry["id"])
                exists = session.execute(stmt).first()
                if not exists:
                    new_entry = TimeEntries(
                        id=entry["id"],
                        user=player,
                        user_id=user[0].id,
                        user_clockify_id=user[0].clockify_id,
                        project=project_name,
                        project_id=entry["projectId"],
                        start=entry["timeInterval"]["start"],
                        end=entry["timeInterval"]["end"],
                        duration=self.convert_clockify_duration(
                            entry["timeInterval"]["duration"]
                        ),
                    )
                    session.add(new_entry)
                else:
                    stmt = (
                        update(TimeEntries)
                        .where(TimeEntries.id == entry["id"])
                        .values(
                            user_clockify_id=user[0].clockify_id,
                            user=player,
                            user_id=user[0].id,
                            project=project_name,
                            project_id=entry["projectId"],
                            start=entry["timeInterval"]["start"],
                            end=entry["timeInterval"]["end"],
                            duration=self.convert_clockify_duration(
                                entry["timeInterval"]["duration"]
                            ),
                        )
                    )
                    session.execute(stmt)
                session.commit()
            except Exception as e:
                session.rollback()
                logger.info("Error adding new entry: " + str(e))
            # logger.info(entry["id"])
            # exit()
        return

    # def add_time_entry_from_excel(self, player, game, day, time):
    #     user = self.get_user(name=player)
    #     try:
    #         session = sessionmaker(bind=engine)()
    #         # print("Adding excel time")
    #         start_date = datetime.datetime(2023, 1, 1)
    #         start_date = start_date + datetime.timedelta(days=day - 9)
    #         end_date = start_date + datetime.timedelta(
    #             seconds=int(time.total_seconds())
    #         )
    #         start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    #         end_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    #         excel_id = (
    #             "excel"
    #             + "-"
    #             + player
    #             + "-"
    #             + game.replace(" ", "")
    #             + "-"
    #             + str(day - 8)
    #         )
    #         project_id = clockify.get_project_id_by_strict_name(
    #             game, config.CLOCKIFY_ADMIN_API_KEY
    #         )
    #         # project_name = clockify.get_project(entry["projectId"])["name"]
    #         stmt = select(TimeEntries).where(TimeEntries.id == excel_id)
    #         exists = session.execute(stmt).first()
    #         # print(start_date)
    #         # print(end_date)
    #         # print(int(time.total_seconds()))
    #         # print(excel_id)
    #         # print(exists)
    #         # exit()
    #         if not exists:
    #             new_entry = TimeEntries(
    #                 id=excel_id,
    #                 user=player,
    #                 user_id=user[0].id,
    #                 user_clockify_id=user[0].clockify_id,
    #                 project=game,
    #                 project_id=project_id,
    #                 start=start_date,
    #                 end=end_date,
    #                 duration=int(time.total_seconds()),
    #             )
    #             session.add(new_entry)
    #             # session.commit()
    #         # else:
    #         #     stmt = (
    #         #         update(TimeEntries)
    #         #         .where(TimeEntries.id == excel_id)
    #         #         .values(
    #         #             user=player,
    #         #             user_id=user[0].id,
    #         #             user_clockify_id=user[0].clockify_id,
    #         #             project=game,
    #         #             project_id=project_id,
    #         #             start=start_date,
    #         #             end=end_date,
    #         #             duration=int(time.total_seconds()),
    #         #         )
    #         #     )
    #         #     session.execute(stmt)
    #         session.commit()
    #     except Exception as e:
    #         session.rollback()
    #         logger.info(
    #             "Error adding new entry from Excel: "
    #             + player
    #             + "-"
    #             + game
    #             + "-"
    #             + str(e)
    #         )
    #     finally:
    #         session.close()
    #     return

    # def get_user(self, telegram_id=None, telegram_username=None, name=None):
    #     """Check if user is allowed to use the bot. At least 1 param must be passed

    #     Args:
    #         telegram_id (int/string, optional): Telegram ID. Defaults to None.
    #         telegram_username (string, optional): Telegram username. Defaults to None.
    #         name (string, optional): User name. Defaults to None.

    #     Returns:
    #         Row: If user exists, return User info as SQL row. Else, returns None
    #     """
    #     session = sessionmaker(bind=engine)()
    #     if telegram_id is not None:
    #         stmt = select(User).where(User.telegram_id == telegram_id)
    #         user = session.execute(stmt).first()
    #         if user is None and telegram_username is not None:
    #             stmt = (
    #                 update(User)
    #                 .where(User.telegram_username == telegram_username)
    #                 .values(telegram_id=telegram_id)
    #             )
    #             session.execute(stmt)
    #             stmt = select(User).where(User.telegram_username == telegram_username)
    #             user = session.execute(stmt).first()
    #             session.commit()
    #             session.close()
    #         else:
    #             return None
    #     elif telegram_username is not None:
    #         stmt = select(User).where(User.telegram_username == telegram_username)
    #         user = session.execute(stmt).first()
    #         if user is None and telegram_id is not None:
    #             stmt = (
    #                 update(User)
    #                 .where(User.telegram_id == telegram_id)
    #                 .values(telegram_username=telegram_username)
    #             )
    #             session.execute(stmt)
    #             stmt = select(User).where(User.telegram_username == telegram_username)
    #             user = session.execute(stmt).first()
    #             session.commit()
    #             session.close()
    #         else:
    #             return False
    #         session.commit()
    #         session.close()
    #     elif name is not None:
    #         stmt = select(User).where(User.name == name)
    #         user = session.execute(stmt).first()
    #         session.commit()
    #         session.close()
    #     else:
    #         return False
    #     return user

    # def add_user_bot(self, username, name, user_id):
    #     session = sessionmaker(bind=engine)()
    #     stmt = select(User).where(User.name == name)
    #     user = session.execute(stmt).first()
    #     if not user:
    #         new_user = User(name=name, telegram_username=username, telegram_id=user_id)
    #         session.add(new_user)
    #         # session.commit()
    #     else:
    #         stmt = (
    #             update(User)
    #             .where(User.telegram_id == user_id)
    #             .values(name=user, telegram_username=username)
    #         )
    #         session.execute(stmt)
    #     session.commit()
    #     session.close()

    # def add_user(self, name):
    #     session = sessionmaker(bind=engine)()
    #     stmt = select(User).where(User.name == name)
    #     user = session.execute(stmt).first()
    #     if not user:
    #         new_user = User(name=name)
    #         session.add(new_user)
    #         session.commit()
    #         session.close()

    def game_exists(self, game_name):
        session = sessionmaker(bind=engine)()
        stmt = select(GamesInfo).where(GamesInfo.game == game_name)
        game = session.execute(stmt).first()
        session.close()
        if game:
            return True
        return False

    def add_new_game(
        self,
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
            session = sessionmaker(bind=engine)()
            game = GamesInfo(
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
            session.add(game)
            session.commit()
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                session.rollback()
            else:
                logger.info("Error adding new game: " + str(e))
        finally:
            session.close()

    def update_game(
        self,
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
            session = sessionmaker(bind=engine)()
            stmt = (
                update(GamesInfo)
                .where(GamesInfo.game == game)
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
            session.execute(stmt)
            session.commit()
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def update_total_played_game(self, game, total_played):
        try:
            session = sessionmaker(bind=engine)()
            stmt = (
                update(GamesInfo)
                .where(GamesInfo.game == game)
                .values(played_time=total_played)
            )
            session.execute(stmt)
            session.commit()
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def update_current_ranking_hours_game(self, i, game):
        try:
            session = sessionmaker(bind=engine)()
            stmt = (
                update(GamesInfo)
                .where(GamesInfo.game == game)
                .values(current_ranking=i)
            )
            session.execute(stmt)
            session.commit()
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def update_last_ranking_hours_game(self, i, game):
        try:
            session = sessionmaker(bind=engine)()
            stmt = (
                update(GamesInfo).where(GamesInfo.game == game).values(last_ranking=i)
            )
            session.execute(stmt)
            session.commit()
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def get_current_ranking_games(self):
        try:
            session = sessionmaker(bind=engine)()
            stmt = (
                select(GamesInfo.game)
                .order_by(asc(GamesInfo.current_ranking))
                .limit(11)
            )
            return session.execute(stmt)
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def get_current_ranking_players(self):
        try:
            session = sessionmaker(bind=engine)()
            stmt = select(User.name, User.current_ranking_hours).order_by(
                asc(User.current_ranking_hours)
            )
            return session.execute(stmt)
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def get_last_ranking_games(self):
        try:
            session = sessionmaker(bind=engine)()
            stmt = (
                select(GamesInfo.game).order_by(asc(GamesInfo.last_ranking)).limit(11)
            )
            return session.execute(stmt)
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def get_last_ranking_players(self):
        try:
            session = sessionmaker(bind=engine)()
            stmt = select(User.name, User.last_ranking_hours).order_by(
                asc(User.last_ranking_hours)
            )
            return session.execute(stmt)
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def add_or_update_game_user(self, game_name, player, score, platform, i, seconds):
        session = sessionmaker(bind=engine)()
        try:
            stmt = select(UsersGames).where(
                UsersGames.game == game_name, UsersGames.player == player
            )
            row = session.execute(stmt).first()
            if not row:
                # logger.info(player + " has started new game: " + game_name)
                user_game = UsersGames(
                    game=game_name,
                    player=player,
                    platform=platform,
                    score=score,
                    started_date=datetime.datetime.now().date(),
                    row=i,
                    played_time=seconds,
                    last_update=str(datetime.datetime.now().timestamp()),
                )
                session.add(user_game)
                session.commit()
                return i + 1
            else:
                stmt = (
                    update(UsersGames)
                    .where(UsersGames.game == game_name, UsersGames.player == player)
                    .values(
                        game=game_name,
                        player=player,
                        platform=platform,
                        score=score,
                        row=i,
                        played_time=seconds,
                        # last_update=str(datetime.datetime.now()),
                    )
                )
                session.execute(stmt)
                session.commit()
                return False
            # session.close()
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def game_completed(self, player, game):
        session = sessionmaker(bind=engine)()
        stmt = select(UsersGames).where(
            UsersGames.game == game,
            UsersGames.player == player,
            UsersGames.completed == 1,
        )
        row = session.execute(stmt).first()
        session.close()
        if row:
            return True
        return False

    def complete_game(self, player, game_name, score, time, seconds):
        try:
            session = sessionmaker(bind=engine)()
            stmt = (
                update(UsersGames)
                .where(UsersGames.game == game_name, UsersGames.player == player)
                .values(
                    score=score,
                    played_time=seconds,
                    completed=1,
                    completed_date=datetime.datetime.now().date(),
                )
            )
            session.execute(stmt)
            session.commit()

            completed_games_count = (
                session.query(UsersGames).filter_by(player=player, completed=1).count()
            )

            return completed_games_count
        except Exception as e:
            session.rollback()
            if "Duplicate entry" in str(e) or "UNIQUE" in str(e):
                # logger.info("Logro '" + achievement + "' ya desbloqueado")
                return False
            else:
                raise Exception("Error checking achievement:", e)
        finally:
            session.close()

    def mean_time_game(self, game):
        session = sessionmaker(bind=engine)()
        stmt = select(GamesInfo.mean_time).where(GamesInfo.game == game)
        result = session.execute(stmt).first()
        session.close()
        return result[0]

    def total_played_time_games(self):
        session = sessionmaker(bind=engine)()
        stmt = select(UsersGames.game, func.sum(UsersGames.played_time)).group_by(
            UsersGames.game
        )
        result = session.execute(stmt)
        session.close()
        return result

    def update_current_ranking_hours(self, ranking, player):
        session = sessionmaker(bind=engine)()
        stmt = (
            update(User)
            .where(User.name == player)
            .values(current_ranking_hours=ranking)
        )
        session.execute(stmt)
        session.commit()
        session.close()

    def update_last_ranking_hours(self, ranking, player):
        session = sessionmaker(bind=engine)()
        stmt = (
            update(User).where(User.name == player).values(last_ranking_hours=ranking)
        )
        session.execute(stmt)
        session.commit()
        session.close()

    def player_played_time(self):
        session = sessionmaker(bind=engine)()
        stmt = select(UsersGames.player, func.sum(UsersGames.played_time)).group_by(
            UsersGames.player
        )
        result = session.execute(stmt)
        session.close()
        return result

    def get_played_games(self, player):
        session = sessionmaker(bind=engine)()
        return (
            session.query(
                UsersGames.game,
                UsersGames.platform,
                UsersGames.row,
                UsersGames.played_time,
            )
            .filter_by(player=player)
            .order_by(desc(UsersGames.last_update))
        )

    def last_update(self, date_in_seconds, player, game_row):
        # print(
        #     "Updating row",
        #     game_row,
        #     ":",
        #     datetime.datetime.fromtimestamp(date_in_seconds),
        # )
        session = sessionmaker(bind=engine)()
        stmt = (
            update(UsersGames)
            .where(UsersGames.player == player, UsersGames.row == game_row)
            .values(last_update=date_in_seconds)
        )
        session.execute(stmt)
        session.commit()
        session.close()

    def save_played_days(self, player, played_days):
        try:
            session = sessionmaker(bind=engine)()
            stmt = (
                update(User).where(User.name == player).values(played_days=played_days)
            )
            session.execute(stmt)
            session.commit()
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    ######################
    #### ACHIEVEMENTS ####
    ######################

    def get_achievements_list(self):
        session = sessionmaker(bind=engine)()
        return session.query(
            Achievement.achievement,
        )

    def check_achievement(self, player, achievement):
        session = sessionmaker(bind=engine)()
        try:
            ach = UserAchievements(player=player, achievement=achievement)
            session.add(ach)
            session.commit()
            return False
        except Exception as e:
            session.rollback()
            if "Duplicate entry" in str(e) or "UNIQUE" in str(e):
                # logger.info("Logro '" + achievement + "' ya desbloqueado")
                return True
            else:
                raise Exception("Error checking achievement:", e)
        finally:
            session.close()

    def lose_streak(self, player, streak, date=None):
        session = sessionmaker(bind=engine)()
        if streak == 0:
            stmt = select(User.last_streak).where(User.name == player)
            last = session.execute(stmt).first()
            if last[0] != None and last[0] != 0:
                stmt = (
                    update(User)
                    .where(User.name == player)
                    .values(last_streak=streak, last_streak_date=date)
                )
                session.execute(stmt)
                session.commit()
                return last[0]
        stmt = (
            update(User)
            .where(User.name == player)
            .values(last_streak=streak, last_streak_date=date)
        )
        session.execute(stmt)
        session.commit()
        session.close()
        return False

    def best_streak(self, player, streak, date):
        session = sessionmaker(bind=engine)()
        stmt = select(User.best_streak).where(User.name == player)
        best_streak = session.execute(stmt).first()
        if best_streak[0] is None or best_streak[0] <= streak:
            stmt = (
                update(User)
                .where(User.name == player)
                .values(best_streak=streak, best_streak_date=date)
            )
            session.execute(stmt)
            session.commit()
            session.close()

    def current_streak(self, player, streak):
        session = sessionmaker(bind=engine)()
        stmt = update(User).where(User.name == player).values(current_streak=streak)
        session.execute(stmt)
        session.commit()
        session.close()

    ####################
    #### MY ROUTES #####
    ####################

    def my_top_games(self, player):
        try:
            session = sessionmaker(bind=engine)()
            stmt = (
                select(UsersGames.game, UsersGames.played_time)
                .where(UsersGames.player == player)
                .order_by(desc(UsersGames.played_time))
                .limit(10)
            )
            return session.execute(stmt)
        except Exception as e:
            logger.info(e)

    def my_completed_games(self, player):
        try:
            session = sessionmaker(bind=engine)()
            return session.query(UsersGames).filter_by(player=player, completed=1)
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def my_last_completed_games(self, player):
        try:
            session = sessionmaker(bind=engine)()
            return (
                session.query(UsersGames.game)
                .filter_by(player=player, completed=1)
                .order_by(desc(UsersGames.last_update))
            )
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def my_achievements(self, player):
        try:
            session = sessionmaker(bind=engine)()
            stmt = select(UserAchievements.achievement).where(
                UserAchievements.player == player
            )
            return session.execute(stmt).fetchall()
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def my_streak(self, player):
        try:
            session = sessionmaker(bind=engine)()
            return session.query(
                User.current_streak,
                User.best_streak,
                User.best_streak_date,
            ).filter_by(name=player)
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    ####################
    ####### EXCEL#######
    ####################

    def get_game_excel_row(self, player, game):
        logger.info("Get game row")
        session = sessionmaker(bind=engine)()
        stmt = select(UsersGames.row).where(
            UsersGames.player == player, UsersGames.game == game
        )
        row = session.execute(stmt).first()
        if row is None:
            logger.info("Game " + game + " not in " + player + " list")
            return 0
        else:
            # add row + 2 in order to sum 0 and Excel header
            row = row[0] + 2
            logger.info("Excel row for game " + game + " is " + str(row))
            return row

    def get_games_to_score(self, player):
        logger.info("Get games to score")
        session = sessionmaker(bind=engine)()
        stmt = select(UsersGames.game, UsersGames.score).where(
            UsersGames.player == player, UsersGames.score == None
        )
        return session.execute(stmt).fetchall()

    def get_games_to_complete(self, player):
        logger.info("Get games to score")
        session = sessionmaker(bind=engine)()
        stmt = select(UsersGames.game).where(
            UsersGames.player == player,
            UsersGames.completed == None,
        )
        return session.execute(stmt).fetchall()

    def get_games(self, player):
        logger.info("Get games")
        session = sessionmaker(bind=engine)()
        stmt = select(UsersGames.game).where(UsersGames.player == player)
        return session.execute(stmt).fetchall()

    def get_games_by_last_played(self, player):
        logger.info("Get games to add time")
        session = sessionmaker(bind=engine)()
        return (
            session.query(UsersGames.game)
            .filter_by(player=player)
            .order_by(desc(UsersGames.last_update))
        )

    ######################
    ##### RANKING ########
    ######################

    def get_ranking_games(self):
        try:
            session = sessionmaker(bind=engine)()
            stmt = select(
                GamesInfo.game,
                GamesInfo.played_time,
                GamesInfo.last_ranking,
                GamesInfo.current_ranking,
            ).order_by(desc(GamesInfo.played_time))
            return session.execute(stmt)
        except Exception as e:
            logger.info(e)
        finally:
            session.close()

    def ranking_days(self):
        try:
            session = sessionmaker(bind=engine)()
            return session.query(User.name, User.played_days).order_by(
                desc(User.played_days)
            )
        except Exception as e:
            logger.info(e)

    def ranking_streak(self):
        try:
            session = sessionmaker(bind=engine)()
            return session.query(User.name, User.best_streak).order_by(
                desc(User.best_streak)
            )
        except Exception as e:
            logger.info(e)

    def ranking_current_streak(self):
        try:
            session = sessionmaker(bind=engine)()
            return session.query(User.name, User.current_streak).order_by(
                desc(User.current_streak)
            )
        except Exception as e:
            logger.info(e)

    def ranking_achievements(self):
        session = sessionmaker(bind=engine)()
        return (
            session.query(UserAchievements.player, func.count(UserAchievements.player))
            .group_by(UserAchievements.player)
            .order_by(func.count(UserAchievements.player).desc())
            .all()
        )

    def ranking_num_games(self):
        session = sessionmaker(bind=engine)()
        result = (
            session.query(UsersGames.player, func.count(UsersGames.game))
            .group_by(UsersGames.player)
            .order_by(func.count(UsersGames.game).desc())
            .all()
        )
        return result

    def ranking_completed_games(self):
        session = sessionmaker(bind=engine)()
        return (
            session.query(UsersGames.player, func.count(UsersGames.game))
            .group_by(UsersGames.player)
            .filter_by(completed=1)
            .order_by(func.count(UsersGames.game).desc())
            .all()
        )

    def ranking_last_played_games(self):
        session = sessionmaker(bind=engine)()
        stmt = select(UsersGames.game, UsersGames.played_time).order_by(
            desc(UsersGames.last_update)
        )
        return session.execute(stmt).fetchall()

    def ranking_most_played_games(self):
        session = sessionmaker(bind=engine)()
        stmt = (
            select(GamesInfo.game, GamesInfo.played_time)
            .order_by(desc(GamesInfo.played_time))
            .limit(10)
        )
        return session.execute(stmt).fetchall()

    ################
    #### OTHERS ####
    ################

    def get_last_row_games(self, player):
        session = sessionmaker(bind=engine)()
        stmt = (
            select(UsersGames.row)
            .where(UsersGames.player == player)
            .order_by(desc(UsersGames.row))
        )
        return session.execute(stmt).first()

    def close(self):
        self.session.close()
