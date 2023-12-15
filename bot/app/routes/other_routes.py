import random
from datetime import datetime, timedelta
from difflib import SequenceMatcher

import utils.messages as msgs
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import ContextTypes, ConversationHandler
from utils.logger import logger
from utils.my_utils import MyUtils

utils = MyUtils()


class OtherRoutes:
    # async def info_game(
    #     self, update: Update, context: ContextTypes.DEFAULT_TYPE
    # ) -> int:
    #     utils.log("Info game")
    #     msg = (
    #         'Por favor, introduce el nombre del juego empezando por "/"'
    #         "(tardaré unos segundos en buscarlo, no me seas ansia. Ah, y /cancel para cancelar):"
    #     )
    #     await utils.response_conversation(update, context, msg)
    #     return utils.INFO_GAME

    # async def info_game_response(
    #     self, update: Update, context: ContextTypes.DEFAULT_TYPE
    # ) -> int:
    #     await utils.response_conversation(update, context, "TBI")
    #     return
    #     game_orig = update.message.text
    #     utils.log("Received game " + game_orig)
    #     user = update.message.from_user.first_name
    #     if game_orig == "/cancel" or game_orig.lower() == "cancel":
    #         await utils.reply_message(update, context, "Pos nah. Taluego.")
    #         return ConversationHandler.END
    #     if game_orig == "/menu" or game_orig == "/menu@LaViciacionBot":
    #         msg = (
    #             "No, a ver "
    #             + user
    #             + ", aprende a leer. Tienes que escribir el "
    #             + "nombre del juego empezando por /, no pedir otra vez el menú. "
    #             + "Vuelve a intentarlo, que tú puedes."
    #         )
    #         return await utils.reply_message(update, context, msg)
    #     rawg_info, hltb_info, hltb_main_story = utils.get_game_info(game_orig)
    #     real_name = rawg_info["name"]
    #     slug = rawg_info["slug"]
    #     if rawg_info is None:
    #         return await utils.reply_message(
    #             update, context, "No encuentro ese juego. Prueba otra vez"
    #         )
    #     rawg_info, hltb_info, mean_time = await utils.get_game_info(real_name)
    #     if mean_time is not None:
    #         h_mean = str(mean_time).split(".")[0]
    #         remaining_minutes = mean_time - float(str(mean_time).split(".")[0])
    #         m_mean = round(remaining_minutes * 60)
    #     else:
    #         h_mean = 0
    #         m_mean = 0
    #     if hltb_info is not None:
    #         dev = hltb_info["profile_dev"]
    #     else:
    #         dev = "-"
    #     release_date = rawg_info["released"]
    #     if release_date is not None:
    #         release_date_time = datetime.strptime(release_date, "%Y-%m-%d")
    #         release_date = (
    #             str(release_date_time.day)
    #             + "-"
    #             + str(release_date_time.month)
    #             + "-"
    #             + str(release_date_time.year)
    #         )
    #     else:
    #         release_date = "TBA"
    #     similiraty = SequenceMatcher(None, game_orig.lower(), real_name.lower()).ratio()
    #     if h_mean == 0 and m_mean == 0:
    #         mean_time = "-"
    #     else:
    #         mean_time = f"{h_mean}h{m_mean}m" + "\n"
    #     if rawg_info["metacritic"] is None:
    #         rating = "-"
    #     else:
    #         rating = str(rawg_info["metacritic"]) + "%"
    #     msg = (
    #         "["
    #         + real_name
    #         + "](https://rawg.io/games/"
    #         + slug
    #         + ") "
    #         + str(round(similiraty * 100, 2))
    #         + "%"
    #         + " de fiabilidad\n"
    #     )
    #     msg += "Lanzamiento: " + release_date + "\n"
    #     msg += "Desarrolladora: " + dev + "\n"
    #     msg += "HLTB: " + mean_time + "\n"
    #     msg += "Puntuación: " + rating
    #     return await utils.reply_message(update, context, msg)

    async def random_response(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        if utils.check_valid_chat(update):
            if "SPECIAL WORD" in update.message.text.lower() and utils.random_send(90):
                await utils.reply_message(
                    update, context, "put random message from another function"
                )
