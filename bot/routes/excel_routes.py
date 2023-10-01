from datetime import datetime, timedelta

import gspread
import requests
import telegram
import utils.keyboard as kb
import utils.logger as logger
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.action_logs import ActionLogs
from utils.clockify_api import ClockifyApi
from utils.config import Config
from utils.my_utils import MyUtils

utils = MyUtils()
config = Config()
clockify = ClockifyApi()
# gc = gspread.service_account(filename="la-viciacion-bot-google.json")
# sh = gc.open("Registro de Juegos 2023")

(
    GAME,
    PLATFORM,
    STEAM_ID,
    RELEASE_DATE,
    GENRES,
    MEAN_TIME,
    DEV,
    TIME,
    RATE,
    ROW,
) = range(20, 30)


class ExcelRoutes:
    async def update_info(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        if update.callback_query.message.chat_id < 0:
            await utils.response_conversation(
                update,
                context,
                "Esta opción sólo puede usarse en un chat directo con el bot",
            )
        else:
            logger.info("Update excel menu...")
            # context.user_data["worksheet"] = sh.worksheet(
            #     config.ALLOWED_USERS[context.user_data["username"]]
            # )
            # self.worksheet = sh.worksheet(
            #     config.ALLOWED_USERS[context.user_data["username"]]
            # )
            query = update.callback_query
            await query.answer()
            keyboard = kb.EXCEL_ACTIONS
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
            await utils.reply_message(update, context, "Enga, nos vemos.")
            return ConversationHandler.END
        context.user_data[GAME] = update.message.text
        logger.info("Received game: " + context.user_data[GAME])
        await update.message.reply_text(
            "¿Para qué plataforma?", reply_markup=ReplyKeyboardRemove()
        )
        return utils.EXCEL_ADD_GAME_PLATFORM

    async def add_game_validation(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        try:
            context.user_data[PLATFORM] = update.message.text
            logger.info("Received platform: " + context.user_data[PLATFORM])
            rawg_info, hltb_info, mean_time = await utils.get_game_info(
                context.user_data[GAME]
            )
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
            context.user_data[MEAN_TIME] = mean_time
            msg = "¿Quieres añadir un nuevo juego con los siguiente datos?:\n"
            msg += (
                "Juego: "
                + "["
                + context.user_data[GAME]
                + "](https://rawg.io/games/"
                + rawg_info["slug"]
                + ")\n"
            )
            # msg += "Género: " + str(context.user_data[GENRES]) + "\n"
            msg += "Lanzamiento: " + str(context.user_data[RELEASE_DATE]) + "\n"
            msg += "Desarrolladora: " + str(context.user_data[DEV]) + "\n"
            msg += "Plataforma: " + str(context.user_data[PLATFORM]) + "\n"
            msg += "Steam ID: " + str(context.user_data[STEAM_ID])
            await utils.response_conversation(update, context, "TBI")
            return
            game = requests.get(config.API_URL + "/?????????")
            if game != 0:
                await update.message.reply_text(
                    "Ya tienes añadido "
                    + str(context.user_data[GAME])
                    + " a tu lista de juegos.",
                    reply_markup=ReplyKeyboardRemove(),
                )
                return ConversationHandler.END
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

    async def add_game_confirmation(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        try:
            if "Sí" in str(update.message.text):
                logger.info("Adding new game confirmed")
                await utils.response_conversation(update, context, "TBI")
                return
                # row_num = len(utils.get_last_row(context.user_data["worksheet"])) + 1
                # context.user_data["worksheet"].update_cell(
                #     row_num, 1, context.user_data[GAME]
                # )
                # context.user_data["worksheet"].update_cell(
                #     row_num, 2, context.user_data[DEV]
                # )
                # context.user_data["worksheet"].update_cell(
                #     row_num, 3, context.user_data[RELEASE_DATE]
                # )
                # context.user_data["worksheet"].update_cell(
                #     row_num, 4, context.user_data[PLATFORM]
                # )
                # # context.user_data["worksheet"].update_cell(row_num, 5, context.user_data[GENRES])
                # context.user_data["worksheet"].update_cell(
                #     row_num, 9, context.user_data[STEAM_ID]
                # )
                logger.info("Game " + context.user_data[GAME] + " added"),
                jsonData = {
                    "user": config.ALLOWED_USERS[context.user_data["username"]],
                    "game": context.user_data[GAME],
                }
                logger.info("Send webhook...")
                requests.post(
                    config.N8N_BASE_URL + config.N8N_WH_ADD_GAME,
                    json=jsonData,
                )
                logger.info("Webhook sended...")
                response = requests.post(config.API_URL + "/????????")
                # if not db.game_exists(context.user_data[GAME]):
                #     db.add_new_game(
                #         context.user_data[GAME],
                #         context.user_data[DEV],
                #         context.user_data[RELEASE_DATE],
                #         context.user_data[GENRES],
                #         context.user_data[MEAN_TIME],
                #     )
                # last_row = (
                #     db.get_last_row_games(
                #         config.ALLOWED_USERS[context.user_data["username"]]
                #     )[0]
                #     + 2
                # )
                # print("Last game row:", last_row)
                # await utils.add_or_update_game_user(
                #     context.user_data[GAME],
                #     config.ALLOWED_USERS[context.user_data["username"]],
                #     0,
                #     context.user_data[PLATFORM],
                #     last_row + 1,
                #     0,
                # )
                await update.message.reply_text(
                    "Juego añadido", reply_markup=ReplyKeyboardRemove()
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

    async def rate_game(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Rate game...")
        username = update.message.from_user.username
        await utils.response_conversation(update, context, "TBI")
        return
        games = requests.get(config.API_URL + "???????")
        keyboard = []
        for game in games:
            keyboard.append([game[0]])
        keyboard.append(kb.CANCEL)
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            input_field_placeholder="",
            resize_keyboard=True,
            selective=True,
        )
        await update.message.reply_text(
            "Escoge el juego que quieras puntuar:",
            reply_markup=reply_markup,
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
                await update.message.reply_text(
                    "TBI", reply_markup=ReplyKeyboardRemove()
                )
                return
                # await update.message.reply_text(
                #     "Juego puntuado correctamente", reply_markup=ReplyKeyboardRemove()
                # )
            else:
                await update.message.reply_text(
                    "Cancelada acción de puntuar juego",
                    reply_markup=ReplyKeyboardRemove(),
                )
        except Exception as e:
            await update.message.reply_text("Algo ha salido mal")
        return ConversationHandler.END

    async def update_time(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Add time to game...")
        username = update.message.from_user.username
        await utils.response_conversation(update, context, "TBI")
        return
        games = requests.get(config.API_URL + "/??????")
        keyboard = []
        for game in games:
            keyboard.append([game[0]])
        keyboard.append(kb.CANCEL)
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            input_field_placeholder="",
            resize_keyboard=True,
            selective=True,
        )
        await update.message.reply_text(
            "Escoge un juego, pero ten en cuenta "
            + "que de momento sólo puede añadirse tiempo al día actual:",
            reply_markup=reply_markup,
        )
        return utils.EXCEL_TIME_SELECT_GAME

    async def update_time_game_select(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Received game")
        message = update.message.text
        context.user_data[GAME] = message
        await update.message.reply_text(
            "¿Cuánto tiempo has jugado? El formato debe ser HH:MM.  (/cancel para cancelar)",
            reply_markup=ReplyKeyboardRemove(),
        )
        return utils.EXCEL_ADD_TIME

    async def update_time_time_select(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Received time")
        if update.message.text == "/cancel" or update.message.text.lower() == "cancel":
            await utils.reply_message(update, context, "Pos nah. Taluego.")
            return ConversationHandler.END
        username = update.message.from_user.username
        message = update.message.text
        context.user_data[TIME] = message
        try:
            time_to_add_temp = datetime.strptime(message, "%H:%M")
        except Exception as e:
            await update.message.reply_text("El formato de tiempo no es correcto.")
        col_num = int(datetime.now().strftime("%j")) + 9

        # game_row = result.fetchone()[0]
        # row_num = game_row + 2

        time_to_add = timedelta(
            minutes=time_to_add_temp.minute, hours=time_to_add_temp.hour
        )

        context.user_data[TIME] = time_to_add
        msg = "Juego: *" + context.user_data[GAME] + "*\n"
        msg += "Tiempo añadido: " + str(time_to_add_temp.strftime("%H:%M")) + "\n"
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
        return utils.EXCEL_CONFIRM_TIME

    async def update_time_confirmation(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        try:
            if "Sí" in str(update.message.text):
                logger.info("Add time confirmed")
                username = update.message.from_user.username
                col_num = int(datetime.now().strftime("%j")) + 9

                # game_row = result.fetchone()[0]
                # row_num = game_row + 2
                await update.message.reply_text(
                    "TBI", reply_markup=ReplyKeyboardRemove()
                )
                return
                # await update.message.reply_text(
                #     "Tiempo añadido", reply_markup=ReplyKeyboardRemove()
                # )
                return ConversationHandler.END
            else:
                await update.message.reply_text(
                    "Operación cancelada", reply_markup=ReplyKeyboardRemove()
                )
                return ConversationHandler.END
        except Exception as e:
            logger.info(e)
            await update.message.reply_text("Algo ha salido mal al añadir el tiempo")
            return ConversationHandler.END

    async def complete_game(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Complete game...")
        username = update.message.from_user.username
        await utils.response_conversation(update, context, "TBI")
        return
        games = requests.get(config.API_URL + "/??????")
        keyboard = []
        for game in games:
            keyboard.append([game[0]])
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

                # game_row = result.fetchone()[0]
                # row_num = game_row + 2
                await utils.response_conversation(update, context, "TBI")
                return
                response = requests.patch(config.API_URL + "/???????")
                await update.message.reply_text(
                    "Juego marcado como completado", reply_markup=ReplyKeyboardRemove()
                )

            else:
                await update.message.reply_text(
                    "Cancelada acción de completar juego",
                    reply_markup=ReplyKeyboardRemove(),
                )
        except Exception as e:
            await update.message.reply_text("Algo ha salido mal")
        return ConversationHandler.END

    async def active_timer(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Active timer select game....")
        username = update.message.from_user.username
        if username not in config.CLOCKIFY_USERS_API:
            await update.message.reply_text(
                "No tienes acceso a esta funcionalidad. Ponte en contacto con el administrador.",
                reply_markup=ReplyKeyboardRemove(),
            )
            return ConversationHandler.END
        await utils.response_conversation(update, context, "TBI")
        return
        games = requests.get(config.API_URL + "/??????")
        keyboard = []
        for game in games:
            keyboard.append([game[0]])
        keyboard.append(kb.CANCEL)
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            input_field_placeholder="",
            resize_keyboard=True,
            selective=True,
        )
        await update.message.reply_text(
            "Escoge un juego para iniciar el contador de tiempo:",
            reply_markup=reply_markup,
        )
        return utils.EXCEL_START_TIMER

    async def active_timer_validation(
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
            "¿Seguro que quieres inciar el timer en el juego *"
            + message
            + "*?"
            + "En el caso de tener el timer activado, se parará para iniciar este (El registro previo de tiempo se "
            "añadirá normalmente)",
            reply_markup=reply_markup,
            parse_mode=telegram.constants.ParseMode.MARKDOWN,
        )
        return utils.EXCEL_START_TIMER_COMPLETED

    async def active_timer_confirmation(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        try:
            if "Sí" in str(update.message.text):
                logger.info("Start timer confirmed")
                response = clockify.active_clockify_timer(
                    context.user_data[GAME], context.user_data["username"]
                )
                if response == clockify.RESPONSE_OK:
                    await update.message.reply_text(
                        "Timer del juego iniciado", reply_markup=ReplyKeyboardRemove()
                    )
                elif response == clockify.USER_NOT_EXISTS:
                    await update.message.reply_text(
                        "El usuario no esta activado en Clockify",
                        reply_markup=ReplyKeyboardRemove(),
                    )
                elif response == clockify.API_USER_NOT_ADDED:
                    await update.message.reply_text(
                        "El usuario no tiene acceso a las funcionalidades del timer via bot, ponte en contacto con el "
                        "administrador para solicitar acceso",
                        reply_markup=ReplyKeyboardRemove(),
                    )
            else:
                await update.message.reply_text(
                    "Cancelada acción de inciar timer",
                    reply_markup=ReplyKeyboardRemove(),
                )
        except Exception as e:
            await update.message.reply_text(
                "Algo ha salido mal", reply_markup=ReplyKeyboardRemove()
            )
        return ConversationHandler.END

    async def stop_timer(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Stop timer...")
        username = update.message.from_user.username
        if username not in config.CLOCKIFY_USERS_API:
            await update.message.reply_text(
                "No tienes acceso a esta funcionalidad. Ponte en contacto con el administrador.",
                reply_markup=ReplyKeyboardRemove(),
            )
            return ConversationHandler.END
        keyboard = kb.YES_NO
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            input_field_placeholder="",
            resize_keyboard=True,
            selective=True,
        )
        await update.message.reply_text(
            "¿Seguro que quieres parar el timer actualmente activo?",
            reply_markup=reply_markup,
            parse_mode=telegram.constants.ParseMode.MARKDOWN,
        )
        return utils.EXCEL_STOP_TIMER

    async def stop_timer_confirmation(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        try:
            if "Sí" in str(update.message.text):
                logger.info("Stop timer confirmed....")
                response = clockify.stop_active_clockify_timer(
                    context.user_data["username"]
                )
                if response == clockify.RESPONSE_OK:
                    await update.message.reply_text(
                        "Timer del juego parado", reply_markup=ReplyKeyboardRemove()
                    )
                elif response == clockify.ERROR_TIMER_ACTIVE:
                    await update.message.reply_text(
                        "No tienes ningun timer activado",
                        reply_markup=ReplyKeyboardRemove(),
                    )
                elif response == clockify.USER_NOT_EXISTS:
                    await update.message.reply_text(
                        "El usuario no esta activado en Clockify",
                        reply_markup=ReplyKeyboardRemove(),
                    )
                elif response == clockify.API_USER_NOT_ADDED:
                    await update.message.reply_text(
                        "El usuario no tiene acceso a las funcionalidades del timer via bot, ponte en contacto con el "
                        "administrador para solicitar acceso",
                        reply_markup=ReplyKeyboardRemove(),
                    )
            else:
                await update.message.reply_text(
                    "Cancelada acción de parar timer",
                    reply_markup=ReplyKeyboardRemove(),
                )
        except Exception as e:
            await update.message.reply_text("Algo ha salido mal")
        return ConversationHandler.END

    async def cancel_excel(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        logger.info("Closing excel menu...")
        await update.message.reply_text("Taluego!", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
