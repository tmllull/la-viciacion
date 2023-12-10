import datetime
import json
import logging
import os
import random
import re
import sys

import requests
import telegram
import utils.logger as logger
import utils.messages as msgs
from dotenv import dotenv_values
from howlongtobeatpy import HowLongToBeat
from telegram import Bot, Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.clockify_api import ClockifyApi
from utils.config import Config

config = Config()
clockify = ClockifyApi()


class MyUtils:
    """_summary_"""

    def __init__(self, silent=None):
        self.bot = Bot(config.TELEGRAM_TOKEN)
        self.silent = silent
        # Conversation routes
        (
            self.ACTIVATE_ACCOUNT,
            self.MAIN_MENU,
            self.MY_ROUTES,
            self.RANKING_ROUTES,
            self.INFO_GAME,
            self.SEND_MESSAGE,
            self.EXCEL_STUFF,
            self.EXCEL_TIME_SELECT_GAME,
            self.EXCEL_ADD_TIME,
            self.EXCEL_CONFIRM_TIME,
            self.EXCEL_COMPLETE_GAME,
            self.EXCEL_CONFIRM_COMPLETED,
            self.EXCEL_ADD_GAME,
            self.EXCEL_ADD_GAME_PLATFORM,
            self.EXCEL_ADD_GAME_CONFIRMATION,
            self.EXCEL_RATE_GAME,
            self.EXCEL_RATE_GAME_RATING,
            self.EXCEL_CONFIRM_RATE,
            self.EXCEL_START_TIMER,
            self.EXCEL_START_TIMER_COMPLETED,
            self.EXCEL_STOP_TIMER,
        ) = range(21)

    def make_request(self, method, url, json=None):
        headers = {"x-api-key": config.API_KEY}
        response = requests.request(method, url=url, headers=headers, json=json)
        return response

    def make_clockify_request(self, method, url, json=None):
        headers = {"X-API-KEY": config.CLOCKIFY_ADMIN_API_KEY}
        response = requests.request(method, url=url, headers=headers, json=json)
        return response

    # def api_headers(self):
    #     return {"x-api-key": config.API_KEY}

    async def send_message(self, msg):
        async with self.bot:
            # msg = self.format_text_for_md2(msg)
            await self.bot.send_message(
                chat_id=config.TELEGRAM_GROUP_ID,
                text=msg,
                parse_mode=telegram.constants.ParseMode.MARKDOWN,
            )

    async def send_admin_message(self, msg):
        async with self.bot:
            # msg = self.format_text_for_md2(msg)
            await self.bot.send_message(
                chat_id=config.TELEGRAM_ADMIN_CHAT_ID,
                text=msg,
                parse_mode=telegram.constants.ParseMode.MARKDOWN,
            )

    async def send_photo(self, msg, picture_url):
        async with self.bot:
            # msg = self.format_text_for_md2(msg)
            await self.bot.send_photo(
                chat_id=config.TELEGRAM_GROUP_ID,
                caption=msg,
                photo=picture_url,
                parse_mode=telegram.constants.ParseMode.MARKDOWN,
            )

    def check_valid_chat(self, update: Update) -> bool:
        try:
            username = update.message.from_user.username
            # user_id = update.message.from_user.id
            chat_id = update.message.chat_id
            if chat_id < 0:
                if chat_id != config.TELEGRAM_GROUP_ID:
                    return False
                else:
                    return True
            url = config.API_URL + "/users/" + username
            response = self.make_request("GET", url)
            if response.status_code == 200:
                # user = {"username": username, "telegram_id": user_id}
                # url = config.API_URL + "/users"
                # response = self.make_request("PUT", url, json=user)
                # logger.info(response.json())
                return response.json()
            else:
                logger.info("Error on request to check valid chat!")
                logger.info(response.json())
                return False
        except Exception as e:
            logger.info("Error checking valid chat: " + str(e))

    async def reply_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, msg
    ) -> None:
        await update.message.reply_text(
            msg,
            disable_notification=True,
            disable_web_page_preview=None,
            parse_mode=telegram.constants.ParseMode.MARKDOWN,
        )
        return ConversationHandler.END

    async def response_conversation(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, msg
    ):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            msg, parse_mode=telegram.constants.ParseMode.MARKDOWN
        )
        return ConversationHandler.END

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        name = update.message.from_user.first_name
        msg = msgs.start(name)
        await self.reply_message(update, context, msg)

    async def info_dev(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        chat_id = update.message.chat_id
        await self.reply_message(update, context, chat_id)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        msg = msgs.command_list
        await self.reply_message(update, context, msg)

    def convert_time_to_hours(self, seconds):
        if seconds is None:
            return "0h0m"
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

    def convert_hours_minutes_to_seconds(self, time) -> int:
        if time is None:
            return 0
        return time * 3600

    def random_send(self, percent):
        return random.randrange(100) <= percent

    def format_text_for_md2(self, text):
        # if "](" not in text:
        #     text = (
        #         text.replace("(", "\(")
        #         .replace(")", "\)")
        #         .replace("[", "\[")
        #         .replace("]", "\]")
        #     )
        text = (
            text.replace(".", "\.")
            .replace("!", "\!")
            .replace("-", "\-")
            .replace("+", "\+")
            .replace("=", "\=")
            .replace("(", "\(")
            .replace(")", "\)")
            .replace("[", "\[")
            .replace("]", "\]")
        )
        return text

    def platform(self, platform: str):
        if "switch" in platform:
            platform = platform.replace("switch", "Switch")
        if "nintendo" in platform:
            platform = platform.replace("nintendo", "Nintendo")
        if "steam" in platform:
            platform = platform.replace("steam", "Steam")
        if "playstation" in platform:
            platform = platform.replace("playstation", "playStation")
        if "Playstation" in platform:
            platform = platform.replace("Playstation", "playStation")
        if "xbox" in platform.lower():
            platform = platform.replace("xbox", "Xbox")
        if "pc" in platform.lower():
            platform = platform.replace("pc", "PC")
        if "Pc" in platform.lower():
            platform = platform.replace("Pc", "PC")
        return platform

    def load_json_response(self, response):
        return json.loads(json.dumps(response))

    # async def notify_new_game(
    #     self, player, game, slug, picture_url, platform, total_games
    # ):
    #     logger.info("TBI")
    #     return
    #     if not self.silent:
    #         m_text = " ha empezado su juego nº " + str(total_games) + ": "
    #         msg = (
    #             "*"
    #             + player
    #             + "*"
    #             + m_text
    #             + "["
    #             + game
    #             + "](https://rawg.io/games/"
    #             + slug
    #             + ") para "
    #             + str(platform.strip())
    #             + "."
    #         )
    #         try:
    #             await self.send_photo(msg, picture_url)
    #         except Exception as e:
    #             print(e)
    #             await self.send_message(msg)

    # async def add_new_game(self, game):
    #     logger.info("TBI")
    #     return
    #     try:
    #         logger.info("Adding game " + game)
    #         mean_time = "0"
    #         released = ""
    #         genres = ""
    #         real_name = ""
    #         steam_id = ""
    #         rawg_info, hltb_info, hltb_main_story = await self.get_game_info(game)
    #         if rawg_info is not None:
    #             try:
    #                 steam_id = hltb_info["profile_steam"]
    #             except Exception:
    #                 steam_id = ""
    #             if rawg_info["released"] is not None:
    #                 released = datetime.datetime.strptime(
    #                     rawg_info["released"], "%Y-%m-%d"
    #                 ).date()
    #             else:
    #                 released = None
    #             for genre in rawg_info["genres"]:
    #                 genres += genre["name"] + ","
    #             genres = genres[:-1]

    #         dev = ""
    #         picture_url = rawg_info["background_image"]
    #         if hltb_info is not None:
    #             dev = hltb_info["profile_dev"]
    #         clockify_project = clockify.add_project(game)
    #         project_id = clockify.get_project_id_by_strict_name(
    #             game, config.CLOCKIFY_ADMIN_API_KEY
    #         )
    #         total_games = self.db.add_new_game(
    #             game,
    #             dev,
    #             steam_id,
    #             released,
    #             genres,
    #             hltb_main_story,
    #             project_id,
    #             picture_url,
    #         )
    #         # clockify_project = clockify.add_project(game)
    #         # logger.info(clockify_project)
    #     except Exception as e:
    #         if "Duplicate" not in str(e):
    #             logger.exception(e)

    # async def complete_game(
    #     self, player, game, score, total_time, formatted_time, seconds
    # ):
    #     logger.info("TBI")
    #     return
    #     try:
    #         total_games = self.db.complete_game(
    #             player, game, score, formatted_time, seconds
    #         )
    #         logger.info(player + " has completed " + game + " in " + str(total_time))
    #         await self.notify_completed_game(player, game, total_games, formatted_time)
    #     except Exception as e:
    #         if "UNIQUE" not in str(e):
    #             logger.exception(e)

    # async def notify_completed_game(self, player, game, total_games, formatted_time):
    #     logger.info("TBI")
    #     return
    #     if not self.silent:
    #         mean_time = float(self.db.mean_time_game(game))
    #         if mean_time > 0:
    #             h_mean = str(mean_time).split(".")[0]
    #             remaining_minutes = mean_time - float(str(mean_time).split(".")[0])
    #             m_mean = round(remaining_minutes * 60)
    #         else:
    #             h_mean = 0
    #             m_mean = 0
    #         m_text = " ha completado su juego nº " + str(total_games) + ": "
    #         msg = "*" + player + "*" + m_text + "_" + game + "_"
    #         msg = msg + " en " + formatted_time + ". "
    #         mean_time = str(h_mean) + "h" + str(m_mean) + "m"
    #         if h_mean != 0 and m_mean != 0:
    #             if formatted_time == mean_time:
    #                 msg = msg + "Y encima ha clavado la media de tiempo: "
    #                 await self.just_in_time(player, game)
    #             else:
    #                 msg = msg + "La media está en "
    #             msg = msg + str(h_mean) + "h" + str(m_mean) + "m."
    #         # print(msg)
    #         await self.send_message(msg)

    # async def just_in_time(self, player, game):
    #     logger.info("TBI")
    #     return
    #     try:
    #         self.db.just_in_time(player)
    #         await self.send_message(msgs.just_in_time(player, game))
    #     except Exception as e:
    #         logger.exception(e)

    # # def convert_clockify_duration(self, duration):
    # #     match = re.match(r"PT(\d+H)?(\d+M)?", duration)
    # #     if match:
    # #         horas_str = match.group(1)
    # #         minutos_str = match.group(2)

    # #         horas = int(horas_str[:-1]) if horas_str else 0
    # #         minutos = int(minutos_str[:-1]) if minutos_str else 0

    # #         # Convertir horas y minutos a segundos
    # #         segundos = horas * 3600 + minutos * 60

    # #         return segundos
    # #     else:
    # #         return 0
