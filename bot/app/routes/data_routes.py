import json
from datetime import datetime, timedelta

import requests
import telegram
import utils.keyboard as kb
import utils.logger as logger
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.clockify_api import ClockifyApi
from utils.config import Config
from utils.my_utils import MyUtils

utils = MyUtils()
config = Config()
clockify = ClockifyApi()

(
    GAME,
    GAME_ID,
    PLATFORM,
    STEAM_ID,
    RELEASE_DATE,
    GENRES,
    AVG_TIME,
    DEV,
    TIME,
    RATE,
    IMAGE_URL,
    TOTAL_PLAYED_GAMES,
    CLOCKIFY_PROJECT_ID,
    SLUG,
) = range(20, 34)


class DataRoutes:
    async def update_data(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        if update.callback_query.message.chat_id < 0:
            await utils.response_conversation(
                update,
                context,
                "Esta opción sólo puede usarse en un chat directo con el bot",
            )
        else:
            logger.info("Update data menu...")
            query = update.callback_query
            await query.answer()
            keyboard = kb.DATA_ACTIONS
            reply_markup = ReplyKeyboardMarkup(
                keyboard,
                one_time_keyboard=True,
                input_field_placeholder="¿Quieres confirmar los datos?",
                resize_keyboard=True,
                selective=True,
            )
            await query.edit_message_text("Accediendo al menú de actualizar datos...")
            await query.message.reply_text(
                "Elije una opción:", reply_markup=reply_markup
            )
            return utils.EXCEL_STUFF

    ##################################
    ########## ADD NEW GAME ##########
    ##################################

    async def add_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        logger.info("Add game...")
        await update.message.reply_text(
            "¿Qué juego quieres añadir? (/cancel para cancelar)",
            reply_markup=ReplyKeyboardRemove(),
        )
        return utils.EXCEL_ADD_GAME

    async def add_game_get_name(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        if "cancel" in update.message.text.lower():
            await utils.reply_message(update, context, "Operación cancelada")
            return ConversationHandler.END
        context.user_data[GAME] = update.message.text
        logger.info("Received game: " + context.user_data[GAME])
        # url = (
        #     config.API_URL
        #     + "/users/"
        #     + str(update.message.from_user.username)
        #     + "/games"
        # )
        # response = utils.make_request("GET", url=url)
        # played_games = response.json()
        # context.user_data[TOTAL_PLAYED_GAMES] = len(played_games)
        # for played_game in played_games:
        #     url = config.API_URL + "/games/" + str(played_game["game_id"])
        #     game_info = utils.make_request("GET", url).json()
        #     game_name = game_info["name"]
        #     if game_name == context.user_data[GAME]:
        #         await update.message.reply_text(
        #             "Ya tienes añadido "
        #             + str(context.user_data[GAME])
        #             + " a tu lista de juegos.",
        #             reply_markup=ReplyKeyboardRemove(),
        #         )
        #         return ConversationHandler.END
        url = config.API_URL + "/utils/platforms"
        platforms = utils.make_request("GET", url).json()
        logger.info(platforms)
        keyboard = []
        # logger.info(played_games)
        for platform in platforms:
            keyboard.append([platform["name"]])
        keyboard.append(kb.CANCEL)
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            input_field_placeholder="",
            resize_keyboard=True,
            selective=True,
        )
        await update.message.reply_text(
            "¿Para qué plataforma?", reply_markup=reply_markup
        )
        return utils.EXCEL_ADD_GAME_PLATFORM

    async def add_game_validation(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        try:
            if "❌" in update.message.text:
                await update.message.reply_text(
                    "Acción cancelada",
                    reply_markup=ReplyKeyboardRemove(),
                )
                return ConversationHandler.END
            context.user_data[PLATFORM] = update.message.text
            logger.info("Received platform: " + context.user_data[PLATFORM])
            url = config.API_URL + "/games/rawg/" + str(context.user_data[GAME])
            response = utils.make_request("GET", url=url)
            rawg_info = response.json()["rawg"]
            hltb_info = response.json()["hltb"]
            if rawg_info is None or hltb_info is None:
                logger.info(
                    "No he encontrado ningún juego o me falta información. Por favor, prueba con otro nombre o añade el juego desde la web."
                )
                await update.message.reply_text(
                    "No he encontrado ningún juego o me falta información. Por favor, prueba con otro nombre o añade el juego desde la web.",
                    parse_mode=telegram.constants.ParseMode.MARKDOWN,
                )
                return ConversationHandler.END
            context.user_data[GAME] = rawg_info["name"]
            context.user_data[RELEASE_DATE] = rawg_info["released"]
            if hltb_info is None:
                steam_id = 0
                context.user_data[DEV] = "-"
            else:
                steam_id = hltb_info["profile_steam"]
                context.user_data[DEV] = hltb_info["profile_dev"]
            if steam_id == 0:
                context.user_data[STEAM_ID] = ""
            else:
                context.user_data[STEAM_ID] = steam_id
            if context.user_data[RELEASE_DATE] is not None:
                release_date_time_temp = datetime.strptime(
                    context.user_data[RELEASE_DATE], "%Y-%m-%d"
                )
                context.user_data[RELEASE_DATE] = datetime.strftime(
                    release_date_time_temp, "%d-%m-%Y"
                )
            else:
                context.user_data[RELEASE_DATE] = ""
            genres = ""
            for genre in rawg_info["genres"]:
                genres += genre["name"] + ","
            context.user_data[GENRES] = genres[:-1]
            context.user_data[AVG_TIME] = hltb_info["comp_main"]
            context.user_data[IMAGE_URL] = rawg_info["background_image"]
            context.user_data[SLUG] = rawg_info["slug"]
            url = (
                config.API_URL
                + "/users/"
                + str(update.message.from_user.username)
                + "/games"
            )
            response = utils.make_request("GET", url=url)
            played_games = response.json()
            context.user_data[TOTAL_PLAYED_GAMES] = len(played_games)
            for played_game in played_games:
                url = config.API_URL + "/games/" + str(played_game["game_id"])
                game_info = utils.make_request("GET", url).json()
                game_name = game_info["name"]
                # logger.info(game_info)
                # await update.message.reply_text(
                #     "Checkoint",
                #     reply_markup=ReplyKeyboardRemove(),
                # )
                # return ConversationHandler.END
                if game_name == context.user_data[GAME]:
                    await update.message.reply_text(
                        "Ya tienes añadido "
                        + str(context.user_data[GAME])
                        + " a tu lista de juegos.",
                        reply_markup=ReplyKeyboardRemove(),
                    )
                    return ConversationHandler.END
            msg = "¿Quieres añadir un nuevo juego con los siguiente datos?:\n"
            msg += (
                "Juego: "
                + "["
                + context.user_data[GAME]
                + "](https://rawg.io/games/"
                + rawg_info["slug"]
                + ")\n"
            )
            msg += "Lanzamiento: " + str(context.user_data[RELEASE_DATE]) + "\n"
            msg += "Desarrolladora: " + str(context.user_data[DEV]) + "\n"
            msg += "Plataforma: " + str(context.user_data[PLATFORM]) + "\n"
            msg += "Steam ID: " + str(context.user_data[STEAM_ID])
            keyboard = kb.YES_NO
            reply_markup = ReplyKeyboardMarkup(
                keyboard,
                one_time_keyboard=True,
                input_field_placeholder="",
                resize_keyboard=True,
                selective=True,
            )
            await update.message.reply_text(
                msg,
                reply_markup=reply_markup,
                disable_web_page_preview=None,
                parse_mode=telegram.constants.ParseMode.MARKDOWN,
            )
            return utils.EXCEL_ADD_GAME_CONFIRMATION
        except Exception as e:
            logger.info("Error durante el proceso: " + str(e))
            await update.message.reply_text(
                "Error durante el proceso: "
                + str(e).replace("(", "\(").replace(")", "\)"),
                parse_mode=telegram.constants.ParseMode.MARKDOWN,
            )
            return ConversationHandler.END

    async def add_game_confirmation(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        try:
            if "Sí" in str(update.message.text):
                logger.info("Add new game confirmed")
                url = config.API_URL + "/utils/platforms"
                platforms = utils.make_request("GET", url).json()
                # logger.info(played_games)
                for platform in platforms:
                    if context.user_data[PLATFORM] == platform["name"]:
                        context.user_data[PLATFORM] = platform["id"]
                endpoint = "/workspaces/{}/projects".format(config.CLOCKIFY_WORKSPACE)
                url = "{0}{1}".format(config.CLOCKIFY_BASEURL, endpoint)
                data = {"name": context.user_data[GAME]}
                # Add game as project on Clockify
                response = utils.make_clockify_request("POST", url, json=data)
                if response.status_code == 400:
                    logger.info("Project exists on Clockify")
                    endpoint = "/workspaces/{}/projects?name={}".format(
                        config.CLOCKIFY_WORKSPACE, context.user_data[GAME]
                    )
                    url = "{0}{1}".format(config.CLOCKIFY_BASEURL, endpoint)
                    response = utils.make_clockify_request("GET", url, json=data)
                    clockify_id = response.json()[0]["id"]
                else:
                    logger.info(response)
                    logger.info("New project created on Clockify")
                    logger.info(response.json())
                    clockify_id = response.json()["id"]
                context.user_data[CLOCKIFY_PROJECT_ID] = clockify_id
                try:
                    release_date = str(
                        datetime.strptime(
                            context.user_data[RELEASE_DATE], "%d-%m-%Y"
                        ).date()
                    )
                except Exception as e:
                    logger.warning("Release date error: " + str(e))
                    release_date = None
                new_game = {
                    "name": context.user_data[GAME],
                    "dev": context.user_data[DEV],
                    "release_date": release_date,
                    "steam_id": str(context.user_data[STEAM_ID]),
                    "image_url": context.user_data[IMAGE_URL],
                    "genres": context.user_data[GENRES],
                    "avg_time": utils.convert_hours_minutes_to_seconds(
                        context.user_data[AVG_TIME]
                    ),
                    "clockify_id": clockify_id,
                    "slug": context.user_data[SLUG],
                }
                logger.info("Adding game to DB...")
                response = utils.make_request(
                    "POST", config.API_URL + "/games", json=new_game
                )
                if response.status_code == 400:
                    logger.info("Game already exists on DB")
                elif response.status_code == 200 or response.status_code == 201:
                    logger.info("New game added")
                else:
                    logger.info("Error adding new game:" + str(response.json()))
                username = update.message.from_user.username
                logger.info("Adding new game for " + username)
                start_game = {
                    "game_id": context.user_data[CLOCKIFY_PROJECT_ID],
                    "platform": context.user_data[PLATFORM],
                }
                response = utils.make_request(
                    "POST",
                    config.API_URL + "/users/" + username + "/new_game",
                    json=start_game,
                )
                if response.status_code == 200:
                    logger.info("Game added")
                    await update.message.reply_text(
                        "Juego añadido", reply_markup=ReplyKeyboardRemove()
                    )
                else:
                    logger.info("Error adding new game to user: " + response.json())
                    await update.message.reply_text(
                        "Error adding new game to user: " + str(response.json()),
                        reply_markup=ReplyKeyboardRemove(),
                    )
                return ConversationHandler.END
            else:
                await update.message.reply_text(
                    "Acción cancelada", reply_markup=ReplyKeyboardRemove()
                )
                return ConversationHandler.END
        except Exception as e:
            await update.message.reply_text(
                "Algo ha salido mal al añadir el juego:" + str(e)
            )
            logger.info(e)
            return ConversationHandler.END

    #############################
    ####### COMPLETE GAME #######
    #############################

    async def complete_game(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Complete game...")
        username = update.message.from_user.username
        url = config.API_URL + "/users/" + username + "/games?completed=false"
        played_games = utils.make_request("GET", url).json()
        # played_games = requests.get(
        #     config.API_URL + "/users/" + username + "/games?completed=false"
        # ).json()
        keyboard = []
        # logger.info(played_games)
        for played_game in played_games:
            url = config.API_URL + "/games/" + str(played_game["game_id"])
            game = utils.make_request("GET", url).json()
            # logger.info(game)
            keyboard.append([game["name"]])
        # games = requests.get(config.API_URL + "/games").json()
        # for game in games:
        #     keyboard.append([game["game"]])
        keyboard.append(kb.CANCEL)
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            input_field_placeholder="",
            resize_keyboard=True,
            selective=True,
        )
        await update.message.reply_text(
            "¿Qué juego acabas de completar?", reply_markup=reply_markup
        )
        return utils.EXCEL_COMPLETE_GAME

    async def complete_game_validation(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Received game")
        message = update.message.text
        context.user_data[GAME] = message
        keyboard = kb.YES_NO
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            input_field_placeholder="",
            resize_keyboard=True,
            selective=True,
        )
        await update.message.reply_text(
            "¿Seguro que quieres marcar el juego *" + message + "* como completado?",
            reply_markup=reply_markup,
            parse_mode=telegram.constants.ParseMode.MARKDOWN,
        )
        return utils.EXCEL_CONFIRM_COMPLETED

    async def complete_game_confirmation(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        try:
            if "Sí" in str(update.message.text):
                logger.info("Complete game confirmed")
                username = context.user_data["username"]
                url = config.API_URL + "/games?name=" + context.user_data[GAME]
                game_data = utils.make_request("GET", url).json()[0]
                logger.info("GAME ID: " + str(game_data["id"]))
                url = (
                    config.API_URL
                    + "/users/"
                    + username
                    + "/complete-game?game_id="
                    + str(game_data["id"])
                )
                response = utils.make_request("PATCH", url)
                if response.status_code == 200:
                    # completed_games = response.json()["completed_games"]
                    # completed_time = response.json()["completion_time"]
                    # avg_time = response.json()["avg_time"]

                    await update.message.reply_text(
                        "Juego"
                        # + str(completed_games)
                        + " marcado como completado",
                        reply_markup=ReplyKeyboardRemove(),
                    )
                else:
                    await update.message.reply_text(
                        "Algo ha salido mal completando el juego: " + response.text,
                        reply_markup=ReplyKeyboardRemove(),
                    )

            else:
                await update.message.reply_text(
                    "Cancelada acción de completar juego",
                    reply_markup=ReplyKeyboardRemove(),
                )
        except Exception as e:
            await update.message.reply_text("Algo ha salido mal: " + str(e))
        return ConversationHandler.END

    #############################
    ######### RATE GAME #########
    #############################

    async def rate_game(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Rate game...")
        username = update.message.from_user.username
        url = config.API_URL + "/users/" + username + "/games"
        played_games = utils.make_request("GET", url).json()
        # played_games = requests.get(
        #     config.API_URL + "/users/" + username + "/games?completed=false"
        # ).json()
        keyboard = []
        games_list = []
        # logger.info(played_games)
        for played_game in played_games:
            url = config.API_URL + "/games/" + str(played_game["game_id"])
            game = utils.make_request("GET", url).json()
            # logger.info(game)
            games_list.append([game["name"]])
        # games = requests.get(config.API_URL + "/games").json()
        # for game in games:
        #     keyboard.append([game["game"]])
        games_list = sorted(games_list)
        for game in games_list:
            keyboard.append(game)
        keyboard.append(kb.CANCEL)
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            input_field_placeholder="",
            resize_keyboard=True,
            selective=True,
        )
        await update.message.reply_text(
            "Escoge el juego que quieras puntuar:", reply_markup=reply_markup
        )
        return utils.EXCEL_RATE_GAME

    async def rate_game_get_name(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        if "cancel" in update.message.text.lower():
            await utils.reply_message(update, context, "Pos nah.")
            return ConversationHandler.END
        context.user_data[GAME] = update.message.text
        logger.info("Received game: " + context.user_data[GAME])
        await update.message.reply_text(
            "¿Qué nota quieres darle? ¡CUIDAO! Si vas "
            + "a poner decimales, hazlo como una persona normal y usa una coma.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return utils.EXCEL_RATE_GAME_RATING

    async def rate_game_get_rating(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Received rating")
        if update.message.text == "/cancel" or update.message.text.lower() == "cancel":
            await utils.reply_message(update, context, "Pos nah. Taluego.")
            return ConversationHandler.END
        message = update.message.text
        context.user_data[RATE] = message
        msg = "Juego: *" + context.user_data[GAME] + "*\n"
        msg += "Puntuación: " + str(context.user_data[RATE])
        keyboard = kb.YES_NO
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            input_field_placeholder="",
            resize_keyboard=True,
            selective=True,
        )
        await update.message.reply_text(
            "¿Quieres confirmar la siguiente información?\n\n" + msg,
            reply_markup=reply_markup,
            parse_mode=telegram.constants.ParseMode.MARKDOWN,
        )
        return utils.EXCEL_CONFIRM_RATE

    async def add_rating_confirmation(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        try:
            if "Sí" in str(update.message.text):
                logger.info("Rate game confirmed")
                username = context.user_data["username"]
                url = config.API_URL + "/games?name=" + context.user_data[GAME]
                game_data = utils.make_request("GET", url).json()[0]
                logger.info("GAME ID: " + str(game_data["id"]))
                url = (
                    config.API_URL
                    + "/users/"
                    + username
                    + "/rate-game?game_id="
                    + game_data["id"]
                    + "&score="
                    + context.user_data[RATE]
                )
                logger.info(url)
                response = utils.make_request("PATCH", url)
                if response.status_code == 200:
                    # completed_games = response.json()["completed_games"]
                    # completed_time = response.json()["completion_time"]
                    # avg_time = response.json()["avg_time"]

                    await update.message.reply_text(
                        "Juego"
                        # + str(completed_games)
                        + " puntuado correctamente.",
                        reply_markup=ReplyKeyboardRemove(),
                    )
                else:
                    await update.message.reply_text(
                        "Algo ha salido mal completando el juego: " + response.text,
                        reply_markup=ReplyKeyboardRemove(),
                    )
            else:
                await update.message.reply_text(
                    "Cancelada acción de puntuar juego",
                    reply_markup=ReplyKeyboardRemove(),
                )
        except Exception as e:
            await update.message.reply_text("Algo ha salido mal")
        return ConversationHandler.END

    ####################
    ##### ADD TIME #####
    ####################

    # async def add_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    #     logger.info("Add time to game...")
    #     username = update.message.from_user.username
    #     await utils.response_conversation(update, context, "TBI")
    #     return
    #     games = requests.get(config.API_URL + "/??????")
    #     keyboard = []
    #     for game in games:
    #         keyboard.append([game[0]])
    #     keyboard.append(kb.CANCEL)
    #     reply_markup = ReplyKeyboardMarkup(
    #         keyboard,
    #         one_time_keyboard=True,
    #         input_field_placeholder="",
    #         resize_keyboard=True,
    #         selective=True,
    #     )
    #     await update.message.reply_text(
    #         "Escoge un juego, pero ten en cuenta "
    #         + "que de momento sólo puede añadirse tiempo al día actual:",
    #         reply_markup=reply_markup,
    #     )
    #     return utils.EXCEL_TIME_SELECT_GAME

    # async def add_time_game_select(
    #     self, update: Update, context: ContextTypes.DEFAULT_TYPE
    # ) -> int:
    #     logger.info("Received game")
    #     message = update.message.text
    #     context.user_data[GAME] = message
    #     await update.message.reply_text(
    #         "¿Cuánto tiempo has jugado? El formato debe ser HH:MM.  (/cancel para cancelar)",
    #         reply_markup=ReplyKeyboardRemove(),
    #     )
    #     return utils.EXCEL_ADD_TIME

    # async def add_time_time_select(
    #     self, update: Update, context: ContextTypes.DEFAULT_TYPE
    # ) -> int:
    #     logger.info("Received time")
    #     if update.message.text == "/cancel" or update.message.text.lower() == "cancel":
    #         await utils.reply_message(update, context, "Pos nah. Taluego.")
    #         return ConversationHandler.END
    #     username = update.message.from_user.username
    #     message = update.message.text
    #     context.user_data[TIME] = message
    #     try:
    #         time_to_add_temp = datetime.strptime(message, "%H:%M")
    #     except Exception as e:
    #         await update.message.reply_text("El formato de tiempo no es correcto.")
    #     col_num = int(datetime.now().strftime("%j")) + 9

    #     # game_row = result.fetchone()[0]
    #     # row_num = game_row + 2

    #     time_to_add = timedelta(
    #         minutes=time_to_add_temp.minute, hours=time_to_add_temp.hour
    #     )

    #     context.user_data[TIME] = time_to_add
    #     msg = "Juego: *" + context.user_data[GAME] + "*\n"
    #     msg += "Tiempo añadido: " + str(time_to_add_temp.strftime("%H:%M")) + "\n"
    #     keyboard = kb.YES_NO
    #     reply_markup = ReplyKeyboardMarkup(
    #         keyboard,
    #         one_time_keyboard=True,
    #         input_field_placeholder="",
    #         resize_keyboard=True,
    #         selective=True,
    #     )
    #     await update.message.reply_text(
    #         "¿Quieres confirmar la siguiente información?\n\n" + msg,
    #         reply_markup=reply_markup,
    #         parse_mode=telegram.constants.ParseMode.MARKDOWN,
    #     )
    #     return utils.EXCEL_CONFIRM_TIME

    # async def add_time_confirmation(
    #     self, update: Update, context: ContextTypes.DEFAULT_TYPE
    # ) -> int:
    #     try:
    #         if "Sí" in str(update.message.text):
    #             logger.info("Add time confirmed")
    #             username = update.message.from_user.username

    #             await update.message.reply_text(
    #                 "TBI", reply_markup=ReplyKeyboardRemove()
    #             )
    #             return
    #             # await update.message.reply_text(
    #             #     "Tiempo añadido", reply_markup=ReplyKeyboardRemove()
    #             # )
    #             return ConversationHandler.END
    #         else:
    #             await update.message.reply_text(
    #                 "Operación cancelada", reply_markup=ReplyKeyboardRemove()
    #             )
    #             return ConversationHandler.END
    #     except Exception as e:
    #         logger.info(e)
    #         await update.message.reply_text("Algo ha salido mal al añadir el tiempo")
    #         return ConversationHandler.END

    # async def active_timer(
    #     self, update: Update, context: ContextTypes.DEFAULT_TYPE
    # ) -> int:
    #     logger.info("Active timer select game....")
    #     username = update.message.from_user.username
    #     # TODO: TBI
    #     return "TBI"
    #     if username not in config.CLOCKIFY_USERS_API:
    #         await update.message.reply_text(
    #             "No tienes acceso a esta funcionalidad. Ponte en contacto con el administrador.",
    #             reply_markup=ReplyKeyboardRemove(),
    #         )
    #         return ConversationHandler.END
    #     await utils.response_conversation(update, context, "TBI")
    #     return
    #     games = requests.get(config.API_URL + "/??????")
    #     keyboard = []
    #     for game in games:
    #         keyboard.append([game[0]])
    #     keyboard.append(kb.CANCEL)
    #     reply_markup = ReplyKeyboardMarkup(
    #         keyboard,
    #         one_time_keyboard=True,
    #         input_field_placeholder="",
    #         resize_keyboard=True,
    #         selective=True,
    #     )
    #     await update.message.reply_text(
    #         "Escoge un juego para iniciar el contador de tiempo:",
    #         reply_markup=reply_markup,
    #     )
    #     return utils.EXCEL_START_TIMER

    # async def active_timer_validation(
    #     self, update: Update, context: ContextTypes.DEFAULT_TYPE
    # ) -> int:
    #     logger.info("Received game")
    #     message = update.message.text
    #     context.user_data[GAME] = message
    #     keyboard = kb.YES_NO
    #     reply_markup = ReplyKeyboardMarkup(
    #         keyboard,
    #         one_time_keyboard=True,
    #         input_field_placeholder="",
    #         resize_keyboard=True,
    #         selective=True,
    #     )
    #     await update.message.reply_text(
    #         "¿Seguro que quieres inciar el timer en el juego *"
    #         + message
    #         + "*?"
    #         + "En el caso de tener el timer activado, se parará para iniciar este (El registro previo de tiempo se "
    #         "añadirá normalmente)",
    #         reply_markup=reply_markup,
    #         parse_mode=telegram.constants.ParseMode.MARKDOWN,
    #     )
    #     return utils.EXCEL_START_TIMER_COMPLETED

    # async def active_timer_confirmation(
    #     self, update: Update, context: ContextTypes.DEFAULT_TYPE
    # ) -> int:
    #     try:
    #         if "Sí" in str(update.message.text):
    #             logger.info("Start timer confirmed")
    #             response = clockify.active_clockify_timer(
    #                 context.user_data[GAME], context.user_data["username"]
    #             )
    #             if response == clockify.RESPONSE_OK:
    #                 await update.message.reply_text(
    #                     "Timer del juego iniciado", reply_markup=ReplyKeyboardRemove()
    #                 )
    #             elif response == clockify.USER_NOT_EXISTS:
    #                 await update.message.reply_text(
    #                     "El usuario no esta activado en Clockify",
    #                     reply_markup=ReplyKeyboardRemove(),
    #                 )
    #             elif response == clockify.API_USER_NOT_ADDED:
    #                 await update.message.reply_text(
    #                     "El usuario no tiene acceso a las funcionalidades del timer via bot, ponte en contacto con el "
    #                     "administrador para solicitar acceso",
    #                     reply_markup=ReplyKeyboardRemove(),
    #                 )
    #         else:
    #             await update.message.reply_text(
    #                 "Cancelada acción de inciar timer",
    #                 reply_markup=ReplyKeyboardRemove(),
    #             )
    #     except Exception as e:
    #         await update.message.reply_text(
    #             "Algo ha salido mal", reply_markup=ReplyKeyboardRemove()
    #         )
    #     return ConversationHandler.END

    # async def stop_timer(
    #     self, update: Update, context: ContextTypes.DEFAULT_TYPE
    # ) -> int:
    #     logger.info("Stop timer...")
    #     # TODO: TBI
    #     return "TBI"
    #     username = update.message.from_user.username
    #     if username not in config.CLOCKIFY_USERS_API:
    #         await update.message.reply_text(
    #             "No tienes acceso a esta funcionalidad. Ponte en contacto con el administrador.",
    #             reply_markup=ReplyKeyboardRemove(),
    #         )
    #         return ConversationHandler.END
    #     keyboard = kb.YES_NO
    #     reply_markup = ReplyKeyboardMarkup(
    #         keyboard,
    #         one_time_keyboard=True,
    #         input_field_placeholder="",
    #         resize_keyboard=True,
    #         selective=True,
    #     )
    #     await update.message.reply_text(
    #         "¿Seguro que quieres parar el timer actualmente activo?",
    #         reply_markup=reply_markup,
    #         parse_mode=telegram.constants.ParseMode.MARKDOWN,
    #     )
    #     return utils.EXCEL_STOP_TIMER

    # async def stop_timer_confirmation(
    #     self, update: Update, context: ContextTypes.DEFAULT_TYPE
    # ) -> int:
    #     try:
    #         if "Sí" in str(update.message.text):
    #             logger.info("Stop timer confirmed....")
    #             response = clockify.stop_active_clockify_timer(
    #                 context.user_data["username"]
    #             )
    #             if response == clockify.RESPONSE_OK:
    #                 await update.message.reply_text(
    #                     "Timer del juego parado", reply_markup=ReplyKeyboardRemove()
    #                 )
    #             elif response == clockify.ERROR_TIMER_ACTIVE:
    #                 await update.message.reply_text(
    #                     "No tienes ningun timer activado",
    #                     reply_markup=ReplyKeyboardRemove(),
    #                 )
    #             elif response == clockify.USER_NOT_EXISTS:
    #                 await update.message.reply_text(
    #                     "El usuario no esta activado en Clockify",
    #                     reply_markup=ReplyKeyboardRemove(),
    #                 )
    #             elif response == clockify.API_USER_NOT_ADDED:
    #                 await update.message.reply_text(
    #                     "El usuario no tiene acceso a las funcionalidades del timer via bot, ponte en contacto con el "
    #                     "administrador para solicitar acceso",
    #                     reply_markup=ReplyKeyboardRemove(),
    #                 )
    #         else:
    #             await update.message.reply_text(
    #                 "Cancelada acción de parar timer",
    #                 reply_markup=ReplyKeyboardRemove(),
    #             )
    #     except Exception as e:
    #         await update.message.reply_text("Algo ha salido mal")
    #     return ConversationHandler.END

    async def cancel_data(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Closing excel menu...")
        await update.message.reply_text("Taluego!", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
