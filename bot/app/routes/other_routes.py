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
from utils.action_logs import ActionLogs
from utils.logger import logger
from utils.my_utils import MyUtils

utils = MyUtils()


class OtherRoutes:
    # async def recommender(
    #     self, update: Update, context: ContextTypes.DEFAULT_TYPE
    # ) -> None:
    #     utils.log("Recommender")
    #     #db.log(context.user_data["user"], ActionLogs.RECOMMENDER)
    #     query = update.callback_query
    #     username = query.from_user.username
    #     db.cursor.execute(dbq.total_games)
    #     total_games = db.cursor.fetchone()[0]
    #     db.cursor.execute(
    #         dbq.games_not_played_by_user, (utils.ALLOWED_USERS[username],)
    #     )
    #     games_temp = db.cursor.fetchall()
    #     db.cursor.execute(dbq.played_games, (utils.ALLOWED_USERS[username],))
    #     played_games_temp = db.cursor.fetchall()
    #     played_games = []
    #     for game in played_games_temp:
    #         played_games.append(game[0])
    #     # logger.info(str(played_games))
    #     random.shuffle(games_temp)
    #     games = []
    #     for game_temp in games_temp:
    #         if not any(game_temp[0] == game[0] for game in games):
    #             games.append(game_temp)
    #     random.shuffle(games)
    #     msg = (
    #         "Aquí tienes una lista de 5 juegos (de los "
    #         + str(total_games)
    #         + " que conozco) a los que no has jugado:\n"
    #     )
    #     i = 0
    #     for game in games:
    #         if game[0] not in played_games and game[0] not in msg:
    #             i += 1
    #             msg = msg + game[0] + " (by " + game[1] + ")\n"
    #         if i >= 5:
    #             break

    #     return await utils.response_conversation(update, context, msg)

    async def info_game(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        utils.log("Info game")
        msg = (
            'Por favor, introduce el nombre del juego empezando por "/"'
            "(tardaré unos segundos en buscarlo, no me seas ansia. Ah, y /cancel para cancelar):"
        )
        await utils.response_conversation(update, context, msg)
        return utils.INFO_GAME

    async def info_game_response(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        await utils.response_conversation(update, context, "TBI")
        return
        game_orig = update.message.text
        utils.log("Received game " + game_orig)
        user = update.message.from_user.first_name
        if game_orig == "/cancel" or game_orig.lower() == "cancel":
            await utils.reply_message(update, context, "Pos nah. Taluego.")
            return ConversationHandler.END
        if game_orig == "/menu" or game_orig == "/menu@LaViciacionBot":
            msg = (
                "No, a ver "
                + user
                + ", aprende a leer. Tienes que escribir el "
                + "nombre del juego empezando por /, no pedir otra vez el menú. "
                + "Vuelve a intentarlo, que tú puedes."
            )
            return await utils.reply_message(update, context, msg)
        rawg_info, hltb_info, hltb_main_story = utils.get_game_info(game_orig)
        real_name = rawg_info["name"]
        slug = rawg_info["slug"]
        if rawg_info is None:
            return await utils.reply_message(
                update, context, "No encuentro ese juego. Prueba otra vez"
            )
        rawg_info, hltb_info, mean_time = await utils.get_game_info(real_name)
        if mean_time is not None:
            h_mean = str(mean_time).split(".")[0]
            remaining_minutes = mean_time - float(str(mean_time).split(".")[0])
            m_mean = round(remaining_minutes * 60)
        else:
            h_mean = 0
            m_mean = 0
        if hltb_info is not None:
            dev = hltb_info["profile_dev"]
        else:
            dev = "-"
        release_date = rawg_info["released"]
        if release_date is not None:
            release_date_time = datetime.strptime(release_date, "%Y-%m-%d")
            release_date = (
                str(release_date_time.day)
                + "-"
                + str(release_date_time.month)
                + "-"
                + str(release_date_time.year)
            )
        else:
            release_date = "TBA"
        similiraty = SequenceMatcher(None, game_orig.lower(), real_name.lower()).ratio()
        if h_mean == 0 and m_mean == 0:
            mean_time = "-"
        else:
            mean_time = f"{h_mean}h{m_mean}m" + "\n"
        if rawg_info["metacritic"] is None:
            rating = "-"
        else:
            rating = str(rawg_info["metacritic"]) + "%"
        msg = (
            "["
            + real_name
            + "](https://rawg.io/games/"
            + slug
            + ") "
            + str(round(similiraty * 100, 2))
            + "%"
            + " de fiabilidad\n"
        )
        msg += "Lanzamiento: " + release_date + "\n"
        msg += "Desarrolladora: " + dev + "\n"
        msg += "HLTB: " + mean_time + "\n"
        msg += "Puntuación: " + rating
        return await utils.reply_message(update, context, msg)

    async def random_response(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        if utils.check_valid_chat(update):
            if "silksong" in update.message.text.lower() and utils.random_send(90):
                utils.log("Silksong trigger")
                await utils.reply_message(update, context, msgs.silksong_message())
            if "sanderson" in update.message.text.lower() and utils.random_send(80):
                utils.log("Sanderson trigger")
                await utils.reply_message(
                    update,
                    context,
                    msgs.sanderson_message(update.message.from_user.full_name),
                )
            if (
                "bot" in update.message.text.lower()
                and (
                    " roto" in update.message.text.lower()
                    or " no funciona" in update.message.text.lower()
                    or " de los cojones" in update.message.text.lower()
                    or " inútil" in update.message.text.lower()
                    or " inutil" in update.message.text.lower()
                    or " tonto" in update.message.text.lower()
                    or " mierda" in update.message.text.lower()
                    or " no se entera" in update.message.text.lower()
                    or " no vale" in update.message.text.lower()
                    or " puto" in update.message.text.lower()
                    or " no sabe" in update.message.text.lower()
                    or " no sirve" in update.message.text.lower()
                    or " cascao" in update.message.text.lower()
                    or " jodido" in update.message.text.lower()
                    or " jodio" in update.message.text.lower()
                    or " va mal" in update.message.text.lower()
                    or " funciona mal" in update.message.text.lower()
                    or " rompido" in update.message.text.lower()
                    or " retrasado" in update.message.text.lower()
                    or " retraso" in update.message.text.lower()
                )
                and utils.random_send(90)
                and update.message.from_user.username != "netyaco"
            ):
                logger.info("Bot not works trigger")
                await utils.reply_message(
                    update,
                    context,
                    msgs.bot_not_works_message(update.message.from_user.full_name),
                )
