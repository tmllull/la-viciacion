import json

import requests
import utils.keyboard as kb
import utils.logger as logger
import utils.messages as msgs
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.config import Config
from utils.my_utils import MyUtils

utils = MyUtils()
config = Config()


class BasicRoutes:
    async def menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        logger.info(update.message.from_user.username + " has started conversation...")
        user = utils.check_valid_chat(update)
        if user:
            tg_info = update.message.from_user
            context.user_data["username"] = tg_info.username
            context.user_data["user"] = tg_info.first_name
            context.user_data["user_id"] = tg_info.id
            context.user_data["is_admin"] = user["is_admin"]
            logger.info("User " + tg_info.username + " started the conversation.")
            if context.user_data["is_admin"]:
                keyboard = kb.ADMIN_MENU
            else:
                keyboard = kb.MAIN_MENU
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Hola " + tg_info.first_name + ", elije una opción:",
                reply_markup=reply_markup,
            )
            return utils.MAIN_MENU
        else:
            await utils.reply_message(update, context, msgs.forbiden)

    async def back(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        logger.info("Back")
        await query.answer()
        if context.user_data["is_admin"]:
            keyboard = kb.ADMIN_MENU
        else:
            keyboard = kb.MAIN_MENU
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Elije una opción:", reply_markup=reply_markup
        )
        return utils.MAIN_MENU

    async def end(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Returns `ConversationHandler.END`, which tells the
        ConversationHandler that the conversation is over.
        """
        logger.info("End conversation")
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="Taluego!")
        return ConversationHandler.END

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        logger.info("Getting status...")
        response = requests.get(config.HEALTHCHECKS)
        status_json = json.loads(response.text)
        status = status_json["status"]
        if status == "up":
            status = "El gatete está en plena forma ✅"
        elif status == "down":
            status = "El gatete tiene algunos problemas ❌"
        else:
            status = "El gatete está trabajando, no le molestes ⏱"
        logger.info("End conversation")
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=status)
        return ConversationHandler.END

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        context.user_data["error"] = "Meh"
        await update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text
        )

    async def unknown_text(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        context.user_data["error"] = "Meh"
        await update.message.reply_text(
            "Sorry I can't recognize you , you said '%s'" % update.message.text
        )
