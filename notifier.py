import asyncio
import datetime
import gc
import os
import sys
import time

import pandas as pd
import requests
import utils.logger as logger
from dotenv import dotenv_values
from notifications.achievements import Achievements
from notifications.basic_checks import BasicChecks
from utils.clockify_api import ClockifyApi
from utils.config import Config
from utils.dbalchemy import DatabaseConnector
from utils.my_utils import MyUtils

INIT = False
RESET = False
SILENT = False
DATA_PATH = "data/losdatos.xlsx"
if len(sys.argv) == 2:
    if sys.argv[1] == "init":
        INIT = True
        SILENT = True
    elif sys.argv[1] == "reset":
        RESET = True
        SILENT = True
    elif sys.argv[1] == "silent":
        SILENT = True
    else:
        exit("Invalid argument")


##################
## Main process ##
##################

clockify = ClockifyApi()


async def main():
    config = Config()
    utils = MyUtils()
    start = time.time()
    bc = BasicChecks(SILENT)
    ach = Achievements(SILENT)
    db = DatabaseConnector(INIT, RESET)
    try:
        response = requests.get(config.GOOGLE_DRIVE_URL)
        open(DATA_PATH, "wb").write(response.content)
        xlsx = pd.ExcelFile(DATA_PATH)
        for player in xlsx.sheet_names:
            if INIT or RESET:
                if player not in config.ALLOWED_USERS_RESET.values():
                    continue
            elif player not in config.ALLOWED_USERS.values():
                continue
            logger.info("--- " + player + " ---")
            # if INIT:
            # db.add_user(player)
            # Check if played today
            # if not bc.played_today(player, DATA_PATH):
            #     logger.info("Not played today")
            #     continue
            df = pd.read_excel(DATA_PATH, sheet_name=player)
            await bc.check_games(player, df)
            await ach.check_achievements(player, df, DATA_PATH)
        await bc.update_games_data()
        await ach.check_global_achievements()
        # db.db_to_csv()
        xlsx.close()
        os.remove(DATA_PATH)
        end = time.time()
        logger.info("Elapsed time: " + str(end - start))
    except Exception as e:
        logger.info("Error on notifier: " + str(e))
        await utils.send_admin_message("Error on notifier: " + str(e))


if __name__ == "__main__":
    asyncio.run(main())
