import datetime

import pandas as pd
import utils.logger as logger
import utils.messages as msgs
from utils.clockify_api import ClockifyApi
from utils.config import Config
from utils.dbalchemy import DatabaseConnector
from utils.my_utils import MyUtils

# utils = MyUtils()
db = DatabaseConnector()
clockify = ClockifyApi()
config = Config()


class BasicChecks:
    def __init__(self, silent):
        self.silent = silent
        self.utils = MyUtils(db, silent)

    async def check_games(self, player, data):
        logger.info("Checking games...")
        for i in range(data.index.stop):
            if type(data.loc[i][0]) is not float:
                row = data.loc[i]
                game = str(row[0]).strip()
                if not db.game_exists(game):
                    await self.utils.add_new_game(game)
                platform = self.platform(str(row[3]).strip())
                completed = row[5]
                score = row[7]
                if str(score) == "nan":
                    score = None
                (
                    total_time,
                    formatted_time,
                    seconds,
                    hours,
                    minutes,
                ) = self.utils.calculate_total_time(row, player, game)
                await self.utils.add_or_update_game_user(
                    game, player, score, platform, i, formatted_time, seconds
                )
                if completed:
                    already_completed = db.game_completed(player, game)
                    if not already_completed:
                        await self.utils.complete_game(
                            player, game, score, total_time, formatted_time, seconds
                        )
        # logger.info("Sync Clockify entries...")
        # user = db.get_user(name=player)
        # try:
        #     entries = clockify.get_time_entries(user[0].clockify_id)
        #     db.sync_clockify_entries(player, entries)
        # except Exception as e:
        #     logger.info("Error on sync clockify entries: " + str(e))

    def platform(self, platform):
        if "switch" in platform:
            platform = platform.replace("switch", "Switch")
        if "steam" in platform:
            platform = platform.replace("steam", "Steam")
        if "playstation" in platform:
            platform = platform.replace("playstation", "playStation")
        if "Playstation" in platform:
            platform = platform.replace("Playstation", "PlayStation")
        if "xbox" in platform:
            platform = platform.replace("xbox", "Xbox")
        return platform

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
        for i in range(played_games + 2):
            row = df.loc[i]
            if type(row[0]) is datetime.time:
                return True
        return False

    async def update_games_data(self):
        try:
            logger.info("Update games data...")
            # print("Update games data")
            games = db.total_played_time_games()

            for game in games:
                db.update_total_played_game(game[0], game[1])
            ranking_games = db.get_ranking_games()
            i = 0
            for game in ranking_games:
                try:
                    i += 1
                    db.update_current_ranking_hours_game(i, game[0])
                    if self.silent:
                        db.update_last_ranking_hours_game(i, game[0])
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
