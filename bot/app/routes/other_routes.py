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

    async def random_response(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        if utils.check_valid_chat(update):
            if "SPECIAL WORD" in update.message.text.lower() and utils.random_send(90):
                await utils.reply_message(
                    update, context, "put random message from another function"
                )
