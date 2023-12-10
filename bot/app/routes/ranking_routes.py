import json

import requests
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


class RankingRoutes:
    async def rankings(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        logger.info("Ranking")
        query = update.callback_query
        await query.answer()
        keyboard = kb.RANKING_MENU
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Elije un ranking:", reply_markup=reply_markup
        )
        return utils.RANKING_ROUTES

    async def ranking_hours_player(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("Ranking hours")
        ranking = utils.make_request(
            "GET", config.API_URL + "/statistics/rankings?ranking=hours"
        ).json()
        ranking = utils.load_json_response(ranking[0])
        msg = "Así está el ranking de horas de vicio:\n"
        for i, elem in enumerate(ranking["data"]):
            msg = (
                msg
                + str(i + 1)
                + ". "
                + str(elem["name"])
                + ": "
                + str(utils.convert_time_to_hours(elem["played_time"]))
                + "\n"
            )
        await utils.response_conversation(update, context, msg)

    async def ranking_days_players(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("Ranking days")
        ranking = utils.make_request(
            "GET", config.API_URL + "/statistics/rankings?ranking=days"
        ).json()
        ranking = utils.load_json_response(ranking[0])
        msg = "Así está el ranking de días de vicio:\n"
        for i, elem in enumerate(ranking["data"]):
            msg = (
                msg
                + str(i + 1)
                + ". "
                + str(elem["name"])
                + ": "
                + str(elem["played_days"])
                + "\n"
            )
        await utils.response_conversation(update, context, msg)

    # async def ranking_platform(
    #     self, update: Update, context: ContextTypes.DEFAULT_TYPE
    # ) -> None:
    #     logger.info("Ranking platform")
    #     # db.log(context.user_data["user"], ActionLogs.RANKING_PLATFORM)
    #     db.cursor.execute(dbq.ranking_platform)
    #     result = db.cursor.fetchall()
    #     result = dict(sorted(result, key=lambda x: x[1], reverse=True))
    #     # logger.info(type(result))
    #     msg = "Así está el ranking por plataforma:\n"
    #     i = 0
    #     for elem in result:
    #         if i >= 5:
    #             break
    #         msg = msg + elem + ": " + str(result[elem]) + " juegos\n"
    #         i += 1
    #     await utils.response_conversation(update, context, msg)

    async def ranking_achievements(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("Ranking achievements")
        await utils.response_conversation(update, context, "TBI")
        return
        ach = db.ranking_achievements()
        msg = "El ranking de logros está de la siguiente manera:\n"
        for player, count in ach:
            msg = msg + player + ": " + str(count) + "\n"
        await utils.response_conversation(update, context, msg)

    async def ranking_best_streak(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("Ranking streak")
        ranking = utils.make_request(
            "GET", config.API_URL + "/statistics/rankings?ranking=best_streak"
        ).json()
        ranking = utils.load_json_response(ranking[0])
        msg = "Así va el ranking de racha de días:\n"
        for i, elem in enumerate(ranking["data"]):
            msg = (
                msg
                + str(i + 1)
                + ". "
                + str(elem["name"])
                + ": "
                + str(elem["best_streak"])
                + "\n"
            )
        await utils.response_conversation(update, context, msg)

    async def ranking_current_streak(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("Ranking current streak")
        ranking = utils.make_request(
            "GET", config.API_URL + "/statistics/rankings?ranking=current_streak"
        ).json()
        ranking = utils.load_json_response(ranking[0])
        msg = "Estas són las rachas de días actuales:\n"
        for i, elem in enumerate(ranking["data"]):
            msg = (
                msg
                + str(i + 1)
                + ". "
                + str(elem["name"])
                + ": "
                + str(elem["current_streak"])
                + "\n"
            )
        await utils.response_conversation(update, context, msg)

    async def ranking_ratio(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("Ranking ratio")
        await utils.response_conversation(update, context, "TBI")
        return
        # db.log(context.user_data["user"], ActionLogs.RANKING_RATIO)
        ratio = {}
        played = db.ranking_num_games()
        completed = db.ranking_completed_games()
        msg = "Así está el ratio de juegos completados vs jugados:\n"
        for row in completed:
            ratio[row[0]] = row[1]
        for row in played:
            ratio[row[0]] = ratio[row[0]] / row[1]
        ratio = dict(sorted(ratio.items(), key=lambda x: x[1], reverse=True))
        for player in ratio:
            msg = msg + str(player) + ": " + str(round(ratio[player], 2)) + "\n"

        await utils.response_conversation(update, context, msg)

    async def ranking_user_played_games(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("Ranking played")
        ranking = utils.make_request(
            "GET", config.API_URL + "/statistics/rankings?ranking=user_played_games"
        ).json()
        ranking = utils.load_json_response(ranking[0])
        msg = "Ranking de juegos jugados:\n"
        for i, elem in enumerate(ranking["data"]):
            msg = (
                msg
                + str(i + 1)
                + ". "
                + str(elem["name"])
                + ": "
                + str(elem["played_games"])
                + "\n"
            )

        await utils.response_conversation(update, context, msg)

    async def ranking_completed(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("Ranking completed")
        await utils.response_conversation(update, context, "TBI")
        return
        # db.log(context.user_data["user"], ActionLogs.RANKING_COMPLETED)
        completed_games = db.ranking_completed_games()
        msg = "Ranking de juegos completados:\n"
        for player in completed_games:
            msg = msg + str(player[0]) + ": " + str(player[1]) + "\n"

        await utils.response_conversation(update, context, msg)

    async def ranking_debt(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("Ranking debt")
        await utils.response_conversation(update, context, "Deuda técnica: TBI")
        return
        # debt_list = {}
        # # db.log(context.user_data["user"], ActionLogs.RANKING_DEBT)
        # db.cursor.execute(dbq.players)
        # players = db.cursor.fetchall()
        # for player in players:
        #     debt = 0
        #     db.cursor.execute(dbq.get_played_mean_hours, (player[0],))
        #     played_mean_hours = db.cursor.fetchall()
        #     for row in played_mean_hours:
        #         played = row[0]
        #         mean = float(row[1])
        #         if mean > 0:
        #             h_mean = int(str(mean).split(".")[0]) * 60 * 60
        #             remaining_minutes = mean - float(str(mean).split(".")[0])
        #             m_mean = round(remaining_minutes * 60) * 60
        #             mean_seconds = h_mean + m_mean
        #             if mean_seconds > int(played):
        #                 debt = debt + (mean_seconds - int(played))
        #     debt_list[player[0]] = debt
        # debt_list = dict(sorted(debt_list.items(), key=lambda x: x[1], reverse=True))
        # msg = "Deuda técnica:\n"
        # for player in debt_list:
        #     debt = utils.convert_time_to_hours(debt_list[player])
        #     msg = msg + player + ": " + debt + "\n"
        #     # logger.info(player[0] + "-" + str(debt))

        # await utils.response_conversation(update, context, msg)

    async def ranking_last_played_games(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("Ranking last played")
        ranking = utils.make_request(
            "GET", config.API_URL + "/statistics/rankings?ranking=last_played"
        ).json()
        ranking = utils.load_json_response(ranking[0])
        msg = "Ranking últimos juegos jugados:\n"
        for i, elem in enumerate(ranking["data"]):
            msg = msg + str(i + 1) + ". " + str(elem["name"]) + "\n"
        await utils.response_conversation(update, context, msg)

    async def ranking_most_played(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info("Ranking most played")
        ranking = utils.make_request(
            "GET", config.API_URL + "/statistics/rankings?ranking=most_played_games"
        ).json()
        ranking = utils.load_json_response(ranking[0])
        msg = "Ranking de juegos más jugados:\n"
        for i, elem in enumerate(ranking["data"]):
            msg = (
                msg
                + str(i + 1)
                + ". "
                + str(elem["name"])
                + ": "
                + str(utils.convert_time_to_hours(elem["played_time"]))
                + "\n"
            )
        await utils.response_conversation(update, context, msg)

        # await utils.response_conversation(update, context, "TBI")
        # return
        # db.log(context.user_data["user"], ActionLogs.RANKING_MOST_PLAYED)
        # most_played = db.ranking_most_played_games()
        # msg = "Juegos más jugados:\n"
        # for i, game in enumerate(most_played):
        #     time = utils.convert_time_to_hours(game[1])
        #     msg = (
        #         msg + str(i + 1) + ". *" + str(game[0]) + "*" + " - " + str(time) + "\n"
        #     )
        # await utils.response_conversation(update, context, msg)
