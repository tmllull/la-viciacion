import datetime

import utils.keyboard as kb
import utils.logger as logger
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import ContextTypes, ConversationHandler
from utils.config import Config
from utils.my_utils import MyUtils

utils = MyUtils()
config = Config()


class MyRoutes:
    async def my_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        logger.info("My data")
        # db.log(context.user_data["user"], ActionLogs.MY_DATA)
        await query.answer()
        keyboard = kb.MY_DATA
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="¿Qué quieres consultar?", reply_markup=reply_markup
        )
        return utils.MY_ROUTES

    async def my_games(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        logger.info("My games")
        query = update.callback_query
        username = query.from_user.username
        await utils.response_conversation(update, context, "TBI")
        return
        played_games = db.get_played_games(config.ALLOWED_USERS[username])
        num_games = played_games.count()
        games = ""
        i = 0
        for game in played_games:
            time = utils.convert_time_to_hours(game[3])
            if i < 10:
                games = (
                    games
                    + "- *"
                    + game[0]
                    + "* para _"
                    + game[1]
                    + "_ ("
                    + str(time)
                    + ")\n"
                )
                i += 1
        msg = (
            "Hasta ahora has jugado a *"
            + str(num_games)
            + " juegos*. Estos son los 10 últimos:\n"
            + games
        )
        return await utils.response_conversation(update, context, msg)

    async def my_top_games(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("My top games")
        query = update.callback_query
        username = query.from_user.username
        msg = "Este es tu *top 10*\n"
        await utils.response_conversation(update, context, "TBI")
        return
        top_games = db.my_top_games(config.ALLOWED_USERS[username])
        for game in top_games:
            name = game[0]
            time = str(utils.convert_time_to_hours(game[1]))
            msg = msg + name + " - " + str(time) + "\n"
        return await utils.response_conversation(update, context, msg)

    async def my_completed_games(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("My completed games")
        query = update.callback_query
        username = query.from_user.username
        await utils.response_conversation(update, context, "TBI")
        return
        completed_games = db.my_completed_games(config.ALLOWED_USERS[username]).count()
        # last_completed = db.my_last_completed_games(config.ALLOWED_USERS[username])
        msg = (
            "Hasta ahora has completado *"
            + str(completed_games)
            + " juegos*."
            # + " Estos son los últimos 10:\n"
        )
        # for i, game in enumerate(last_completed):
        #     if i == 10:
        #         break
        #     msg = msg + game[0] + "\n"
        return await utils.response_conversation(update, context, msg)

    async def my_achievements(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("My achievements")
        query = update.callback_query
        username = query.from_user.username
        await utils.response_conversation(update, context, "TBI")
        return
        achievements = db.my_achievements(config.ALLOWED_USERS[username])
        print(achievements)
        achvmts = ""
        achvmts_list = db.get_achievements_list()
        for ach in achievements:
            achvmts = achvmts + "- " + ach[0] + "\n"
        msg = (
            "De momento llevas desbloqueados "
            + str(len(achievements))
            + " de "
            + str(achvmts_list.count())  # + len(ach_sp))
            + " logros:\n"
            + achvmts
        )
        return await utils.response_conversation(update, context, msg)

    async def my_streak(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("My streak")
        # db.log(context.user_data["user"], ActionLogs.MY_STREAK)
        query = update.callback_query
        username = query.from_user.username
        await utils.response_conversation(update, context, "TBI")
        return
        streak_data = db.my_streak(config.ALLOWED_USERS[username])
        msg = "Tu racha actual es de *"
        for row in streak_data:
            msg = (
                msg
                + str(row[0])
                + "* días.\n"
                + "Tu mejor racha fue de *"
                + str(row[1])
                + "* días,"
                + " el "
                + str(row[2])
                + "."
            )
        return await utils.response_conversation(update, context, msg)
