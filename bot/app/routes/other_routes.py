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
    def __init__(self):
        pass
