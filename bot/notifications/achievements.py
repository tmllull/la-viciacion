import datetime

import pandas as pd
import utils.logger as logger
import utils.messages as msgs
from utils.achievements_list import AchievementsList
from utils.dbalchemy import DatabaseConnector
from utils.my_utils import MyUtils

utils = MyUtils()
db = DatabaseConnector()


class Achievements:
    """ """

    def __init__(self, silent):
        self.silent = silent

    async def check_achievements(self, player, data, data_path):
        # Check if played today (or 5am to force sync streaks)
        if (
            not self.played_today(player, data_path)
            and datetime.datetime.now().strftime("%H") != "05"
        ):
            logger.info("Not played today")
            return

        logger.info("Checking achievements...")
        current_time = datetime.datetime.now()
        current_date = datetime.date(
            current_time.year, current_time.month, current_time.day
        )
        start_col = 9
        today_days = int(current_date.strftime("%j"))
        # Rows achievements where game is relevant
        for i in range(data.index.stop):
            row = data.loc[i]
            game = row[0]
            base_time = datetime.time(0, 0, 0)
            total_h = base_time.hour
            total_m = base_time.minute
            if type(game) is not str:
                continue
            for val in range(start_col, start_col + today_days + 1):
                if type(row[val]) is datetime.time:
                    col_date = datetime.datetime(
                        current_time.year, 1, 1
                    ) + datetime.timedelta(days=val - 1)
                    # db.last_update(col_date.timestamp(), player, i)
                    h = row[val].hour
                    m = row[val].minute
                    await self.check_game_achievements(player, game, hours=h, minutes=m)
                    total_h = total_h + h
                    total_m = total_m + m
            db.last_update(col_date.timestamp(), player, i)
            total_time = datetime.timedelta(hours=total_h, minutes=total_m)
            await self.check_game_achievements(player, game, total_time=total_time)
        # Columns achievements like total day time or how many days played
        streak = 0
        empty_day = True
        played_days = 0
        total_sesions = 0
        current_hour = datetime.datetime.now().strftime("%H")
        for name_col, values in data.items():
            total_entries = 0
            base_time = datetime.time(0, 0, 0)
            h = base_time.hour
            m = base_time.minute
            if type(name_col) == datetime.datetime:
                if name_col.date() > current_date:
                    break
                else:
                    played = False
                    row = -1
                    for val in values:
                        row += 1
                        if type(val) is datetime.time:
                            if name_col.date() == current_date:
                                empty_day = False
                            played = True
                            total_sesions += 1
                            total_entries = total_entries + 1
                            h = h + val.hour
                            m = m + val.minute
                    if played:
                        played_days += 1
                    if played and name_col.date() < current_date:
                        streak = streak + 1
                    elif name_col.date() < current_date and not played and streak > 0:
                        streak = 0

                    if current_hour == "05" or self.silent:
                        await self.streak(player, streak, name_col.date())

                    total_time = datetime.timedelta(hours=h, minutes=m)
                    hours, minutes = (
                        total_time.seconds // 3600,
                        total_time.seconds // 60 % 60,
                    )
                    await self.check_day_achievements(
                        player=player,
                        hours=hours,
                        total_entries=total_entries,
                        day=name_col.date(),
                    )

        # Other achievements
        await self.check_played_achievements(player)
        if current_hour == "05" or self.silent:
            await self.lose_streak(player, streak)
        await self.save_played_days(player, played_days)

    def played_today(self, player, data_path):
        if self.silent:
            return True
        current_time = datetime.datetime.now()
        current_date = datetime.date(
            current_time.year, current_time.month, current_time.day
        )
        start_col = 9
        today_days = int(current_date.strftime("%j"))
        today_col = start_col + today_days
        cols = range(today_col - 1, today_col)
        df = pd.read_excel(data_path, sheet_name=player, usecols=cols)
        played_games = db.get_played_games(player)
        for i in range(played_games.count() + 2):
            # logger.info(i)
            row = df.loc[i]
            if type(row[0]) is datetime.time:
                return True
        return False

    async def check_global_achievements(self):
        logger.info("Global rankings and achievements...")
        await self.ranking_hours()
        await self.ranking_games_hours()

    async def ranking_games_hours(self):
        try:
            ranking_games = db.get_ranking_games()
            if not self.silent:
                result = db.get_current_ranking_games()
                current = []
                for game in result:
                    current.append(game[0])
                result = db.get_last_ranking_games()
                last = []
                for game in result:
                    last.append(game[0])
                if current[:10] == last[:10]:
                    logger.info("No changes in games ranking")
                else:
                    logger.info("Changes in games ranking")
                    # logger.info("CURRENT")
                    # logger.info(current)
                    # logger.info("LAST")
                    # logger.info(last)
                    msg = "📣📣 Actualización del ránking de juegos 📣📣\n"
                    i = 0
                    for game in ranking_games:
                        if i <= 10:
                            game_name = game[0]
                            time = game[1]
                            last = game[2]
                            current = game[3]
                            logger.info(game_name + str(i + 1))
                            db.update_last_ranking_hours_game(i + 1, game_name)
                            time = game[1]
                            diff_raw = last - current
                            diff = str(diff_raw)
                            # This adds + to games that up position (positive diff has not + sign)
                            if diff_raw > 0:
                                diff = "+" + diff
                            diff = diff.replace("+", "↑")
                            diff = diff.replace("-", "↓")
                            if diff != "0":
                                game_name = "*" + game_name + "*"
                            else:
                                diff = diff.replace("0", "=")
                            if diff_raw > 1:
                                game_name = "⏫ " + game_name
                            if diff_raw == 1:
                                game_name = "⬆️ " + game_name
                            if diff_raw < 0:
                                game_name = "⬇️ " + game_name
                            # Only to check if game has fall of the top10
                            # Then, always break
                            if i == 10 and "↓" in diff:
                                msg = msg + "----------\n"
                                msg = (
                                    msg
                                    + str(i + 1)
                                    + ". "
                                    + game_name
                                    + ": "
                                    + str(utils.convert_time_to_hours(time))
                                    + " ("
                                    + "💀"
                                    + ")"
                                    + "\n"
                                )
                                break
                            elif i < 10:
                                msg = (
                                    msg
                                    + str(i + 1)
                                    + ". "
                                    + game_name
                                    + ": "
                                    + str(utils.convert_time_to_hours(time))
                                    + " ("
                                    + diff
                                    + ")"
                                    + "\n"
                                )
                            if i == 10:
                                break
                        i += 1
                    if not self.silent:
                        await utils.send_message(msg)
        except Exception as e:
            logger.info("Error in check ranking games: " + str(e))
        logger.info("Sync current ranking with last ranking...")
        ranking_games = db.get_ranking_games()
        i = 1
        for game in ranking_games:
            db.update_last_ranking_hours_game(i, game[0])
            i += 1

    async def ranking_hours(self):
        logger.info("Ranking hours")
        ranking_players = db.player_played_time()
        ranking_players = dict(
            sorted(ranking_players, key=lambda x: x[1], reverse=True)
        )
        for i, elem in enumerate(ranking_players):
            db.update_current_ranking_hours(i + 1, elem)
            if self.silent:
                db.update_last_ranking_hours(i + 1, elem)
        if not self.silent:
            result = db.get_current_ranking_players()
            current = []
            for player in result:
                current.append(player)
            current = dict(sorted(current, key=lambda x: x[1], reverse=True))
            result = db.get_last_ranking_players()
            last = []
            for player in result:
                last.append(player)
            last = dict(sorted(last, key=lambda x: x[1], reverse=True))
            if current == last:
                logger.info("No changes in player ranking")
            else:
                logger.info("Changes in player ranking")
                ranking_players = db.player_played_time()
                ranking_players = dict(
                    sorted(ranking_players, key=lambda x: x[1], reverse=True)
                )
                msg = "📣📣 Actualización del ránking de horas 📣📣\n"
                for i, elem in enumerate(ranking_players):
                    player = elem
                    db.update_last_ranking_hours(i + 1, player)
                    hours = ranking_players[elem]
                    diff_raw = last[player] - current[player]
                    diff = str(diff_raw)
                    # This adds + to games that up position (positive diff has not + sign)
                    if diff_raw > 0:
                        diff = "+" + diff
                    diff = diff.replace("+", "↑")
                    diff = diff.replace("-", "↓")
                    if diff != "0":
                        player = "*" + player + "*"
                    else:
                        diff = diff.replace("0", "=")
                    if diff_raw > 1:
                        player = "⏫ " + player
                    if diff_raw == 1:
                        player = "⬆️ " + player
                    if diff_raw < 0:
                        player = "⬇️ " + player
                    msg = (
                        msg
                        + str(i + 1)
                        + ". "
                        + player
                        + ": "
                        + str(utils.convert_time_to_hours(hours))
                        + " ("
                        + diff
                        + ")"
                        + "\n"
                    )
                if not self.silent:
                    logger.info(msg)
                    await utils.send_message(msg)

    async def check_game_achievements(
        self, player, game, hours=None, minutes=None, total_time=None
    ):
        if (
            hours != None
            and hours >= 8
            and not db.check_achievement(player, AchievementsList.PLAYED_8H_GAME_DAY)
        ):
            logger.info(
                player
                + " ha desbloqueado el logro '"
                + AchievementsList.PLAYED_8H_GAME_DAY
                + "'",
            )
            if not self.silent:
                msg = msgs.played_8h_game_day(player, game)
                logger.info(msg)
                await utils.send_message(msg)

        if (
            hours != None
            and hours == 0
            and (minutes > 0 and minutes <= 5)
            and not db.check_achievement(player, AchievementsList.PLAYED_LESS_5_MIN)
        ):
            logger.info(
                player
                + " ha desbloqueado el logro '"
                + AchievementsList.PLAYED_LESS_5_MIN
                + "'",
            )
            if not self.silent:
                msg = msgs.played_less_5_min(player, game)
                await utils.send_message(msg)

        if total_time != None:
            days, hours, minutes = (
                total_time.days,
                total_time.seconds // 3600,
                total_time.seconds // 60 % 60,
            )
            total_h = days * 24 + hours
            if total_h >= 100 and not db.check_achievement(
                player, AchievementsList.PLAYED_100H_GAME
            ):
                logger.info(
                    player
                    + " ha desbloqueado el logro '"
                    + AchievementsList.PLAYED_100H_GAME
                    + "'",
                )
                if not self.silent:
                    msg = msgs.played_100h_game(player, game)
                    await utils.send_message(msg)

    async def check_day_achievements(
        self, player, hours=None, total_entries=None, day=None
    ):
        if (
            hours != None
            and hours >= 8
            and not db.check_achievement(player, AchievementsList.PLAYED_8H_DAY)
        ):
            logger.info(
                player
                + " ha desbloqueado el logro '"
                + AchievementsList.PLAYED_8H_DAY
                + "'",
            )
            if not self.silent:
                msg = msgs.played_8h_day(player)
                await utils.send_message(msg)

        if (
            hours != None
            and hours >= 12
            and not db.check_achievement(player, AchievementsList.PLAYED_12H_DAY)
        ):
            logger.info(
                player
                + " ha desbloqueado el logro '"
                + AchievementsList.PLAYED_12H_DAY
                + "'",
            )
            if not self.silent:
                msg = msgs.played_12h_day(player)
                await utils.send_message(msg)

        if (
            hours != None
            and hours >= 16
            and not db.check_achievement(player, AchievementsList.PLAYED_16H_DAY)
        ):
            logger.info(
                player
                + " ha desbloqueado el logro '"
                + AchievementsList.PLAYED_16H_DAY
                + "'",
            )
            if not self.silent:
                msg = msgs.played_16h_day(player)
                await utils.send_message(msg)

        if total_entries != None:
            if total_entries >= 5 and not db.check_achievement(
                player, AchievementsList.PLAYED_5_GAMES_DAY
            ):
                logger.info(
                    player
                    + " ha desbloqueado el logro '"
                    + AchievementsList.PLAYED_5_GAMES_DAY
                    + "'",
                )
                if not self.silent:
                    msg = msgs.played_5_games_day(player)
                    await utils.send_message(msg)

            if total_entries >= 10 and not db.check_achievement(
                player, AchievementsList.PLAYED_10_GAMES_DAY
            ):
                logger.info(
                    player
                    + " ha desbloqueado el logro '"
                    + AchievementsList.PLAYED_10_GAMES_DAY
                    + "'",
                )
                if not self.silent:
                    msg = msgs.played_5_games_day(player)
                    await utils.send_message(msg)

    async def check_played_achievements(self, player):
        played_games = db.get_played_games(player).count()
        completed_games = db.my_completed_games(player).count()
        if played_games >= 42 and not db.check_achievement(
            player, AchievementsList.PLAYED_42
        ):
            logger.info(
                player
                + " ha desbloqueado el logro '"
                + AchievementsList.PLAYED_42
                + "'",
            )
            if not self.silent:
                msg = msgs.played_42_games(player)
                await utils.send_message(msg)
        if played_games >= 100 and not db.check_achievement(
            player, AchievementsList.PLAYED_100
        ):
            logger.info(
                player
                + " ha desbloqueado el logro '"
                + AchievementsList.PLAYED_100
                + "'",
            )
            if not self.silent:
                msg = msgs.played_100_games(player)
                await utils.send_message(msg)
        if completed_games >= 42 and not db.check_achievement(
            player, AchievementsList.COMPLETED_42
        ):
            logger.info(
                player
                + " ha desbloqueado el logro '"
                + AchievementsList.COMPLETED_42
                + "'",
            )
            if not self.silent:
                msg = msgs.completed_42_games(player)
                await utils.send_message(msg)
        if completed_games >= 100 and not db.check_achievement(
            player, AchievementsList.COMPLETED_100
        ):
            logger.info(
                player
                + " ha desbloqueado el logro '"
                + AchievementsList.COMPLETED_100
                + "'",
            )
            # if not self.silent:
            #     msg = msgs.completed_42_games(player)
            #     await utils.send_message(msg)

    async def streak(self, player, streak, date):
        try:
            if streak == 7 and not db.check_achievement(
                player, AchievementsList.STREAK_7_DAYS
            ):
                logger.info(
                    player
                    + " ha desbloqueado el logro '"
                    + AchievementsList.STREAK_7_DAYS
                    + "'",
                )
                if not self.silent:
                    msg = msgs.streak_7_days(player)
                    await utils.send_message(msg)

            if streak == 15 and not db.check_achievement(
                player, AchievementsList.STREAK_15_DAYS
            ):
                logger.info(
                    player
                    + " ha desbloqueado el logro '"
                    + AchievementsList.STREAK_15_DAYS
                    + "'",
                )
                if not self.silent:
                    msg = msgs.streak_15_days(player)
                    await utils.send_message(msg)
            if streak == 30 and not db.check_achievement(
                player, AchievementsList.STREAK_30_DAYS
            ):
                logger.info(
                    player
                    + " ha desbloqueado el logro '"
                    + AchievementsList.STREAK_30_DAYS
                    + "'",
                )
                if not self.silent:
                    msg = msgs.streak_30_days(player)
                    await utils.send_message(msg)
            if streak == 66 and not db.check_achievement(
                player, AchievementsList.STREAK_66_DAYS
            ):
                logger.info(
                    player
                    + " ha desbloqueado el logro '"
                    + AchievementsList.STREAK_66_DAYS
                    + "'",
                )
                if not self.silent:
                    msg = msgs.streak_66_days(player)
                    await utils.send_message(msg)
            if streak == 100 and not db.check_achievement(
                player, AchievementsList.STREAK_100_DAYS
            ):
                logger.info(
                    player
                    + " ha desbloqueado el logro '"
                    + AchievementsList.STREAK_100_DAYS
                    + "'",
                )
        except Exception as e:
            if "desbloqueado" not in str(e):
                logger.info("Error checking streak: " + str(e))
        db.best_streak(player, streak, date)
        db.current_streak(player, streak)

    async def lose_streak(self, player, streak):
        try:
            # logger.info("Check streak: "+ streak)
            lose = db.lose_streak(player, streak)
            # logger.info("Lose: "+ lose)
            if lose:
                logger.info(
                    player + " acaba de perder su racha de " + str(lose) + " días."
                )
                if not self.silent and lose >= 10:
                    msg = msgs.lose_streak(player, lose)
                    await utils.send_message(msg)
        except Exception as e:
            logger.warning("Error on lose streak: " + str(e))

    # async def break_streak(self, player, streak):
    #     break_streak = db.break_streak(player, streak)
    #     if break_streak:
    #         logger.info(player, "acaba de superar su mejor racha de", break_streak, "días.")
    #         if not self.silent:
    #             msg = msgs.break_streak(player, break_streak)
    #             await utils.send_message(msg)

    ##########################
    ## SPECIAL ACHIEVEMENTS ##
    ##########################

    ############
    ## OTHERS ##
    ############

    async def save_played_days(self, player, played_days):
        try:
            db.save_played_days(player, played_days)
        except Exception as e:
            logger.info(e)
