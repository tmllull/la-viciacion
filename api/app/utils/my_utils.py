import datetime
import json
import re
from io import BytesIO

import pytz
import requests
import telegram
from dateutil.parser import isoparse
from howlongtobeatpy import HowLongToBeat
from PIL import Image
from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ..config import Config
from ..crud import games, time_entries, users
from ..database import models, schemas
from ..utils import logger
from .achievements import AchievementsElems
from .clockify_api import ClockifyApi

clockify_api = ClockifyApi()
config = Config()


def check_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def validate_password_requirements(password):
    # Length
    if len(password) < 12 or len(password) > 24:
        return False

    # Uppercase
    if not re.search(r"[A-Z]", password):
        return False

    # Lowercase
    if not re.search(r"[a-z]", password):
        return False

    # Number
    if not re.search(r"\d", password):
        return False

    # Special character
    if not re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?/~\\-]", password):
        return False

    return True


def validate_email_format(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, email):
        return True
    else:
        return False


def convert_time_to_hours(seconds) -> str:
    if seconds is None:
        return "0h0m"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h{minutes}m"


def convert_hours_minutes_to_seconds(time) -> int:
    if time is None:
        return 0
    return time * 3600


def convert_date_from_text(date: str):
    logger.debug("Converting date")
    if date is None or date == "":
        return date
    if ":" not in date:
        return datetime.datetime.strptime(date, "%Y-%m-%d")
    return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


def change_timezone_clockify(time) -> str:
    date_time = isoparse(time)
    spain_timezone = pytz.timezone("Europe/Madrid")
    # returns spain_timezone
    return str(date_time.astimezone(spain_timezone).strftime("%Y-%m-%d %H:%M:%S"))


def convert_clockify_duration(duration):
    match = re.match(r"PT(\d+H)?(\d+M)?", duration)
    if match:
        hours_str = match.group(1)
        mins_str = match.group(2)

        hours = int(hours_str[:-1]) if hours_str else 0
        mins = int(mins_str[:-1]) if mins_str else 0

        secs = hours * 3600 + mins * 60

        return secs
    else:
        return 0


def get_last_week_range_dates():
    current_date = datetime.datetime.now()
    first_day_current_week = current_date - datetime.timedelta(
        days=current_date.weekday()
    )
    # last_date_current_week = first_day_current_week + datetime.timedelta(days=6)
    first_day_last_week = first_day_current_week - datetime.timedelta(days=7)
    last_day_last_week = first_day_current_week - datetime.timedelta(days=1)
    # logger.info(first_day_last_week.date())
    # logger.info(last_day_last_week.date())
    return first_day_last_week.date(), last_day_last_week.date()


def get_current_week_range_dates():
    current_date = datetime.datetime.now()
    first_day_current_week = current_date - datetime.timedelta(
        days=current_date.weekday()
    )
    last_day_current_week = first_day_current_week + datetime.timedelta(days=6)
    # logger.info(first_day_current_week.date())
    # logger.info(last_day_current_week.date())
    return first_day_current_week.date(), last_day_current_week.date()


def day_of_the_year(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return date.timetuple().tm_yday


def date_from_day_of_the_year(day):
    current_date = datetime.datetime.now()
    start_date_base = datetime.datetime.strptime(
        str(current_date.year) + "-01-01", "YYYY-MM-DD"
    )
    start_date = datetime.datetime(
        start_date_base.year, start_date_base.month, start_date_base.day
    )
    current_date = start_date + datetime.timedelta(days=day - 1)
    return current_date.strftime("%Y-%m-%d")


def date_from_datetime(datetime: str):
    return datetime.split(" ")[0]


async def get_game_info(game: str):
    # Rawg
    game_request = requests.get(config.RAWG_URL + game)
    try:
        rawg_content = json.loads(game_request.content)["results"][0]
    except Exception:
        rawg_content = None
    # HLTB
    game = game.replace(":", "")
    game = game.replace("/", "")
    results_list = await HowLongToBeat().async_search(game)
    if results_list is not None and len(results_list) > 0:
        best_element = max(results_list, key=lambda element: element.similarity)
        hltb_content = best_element.json_content
    else:
        hltb_content = None

    return {"rawg": rawg_content, "hltb": hltb_content}


async def get_new_game_info(game) -> schemas.NewGame:
    game_name = game["name"]
    project_id = game["id"]
    released = ""
    genres = ""
    steam_id = ""
    dev = ""
    avg_time = 0
    game_info = await get_game_info(game_name)
    rawg_info = game_info["rawg"]
    hltb_info = game_info["hltb"]
    game_name = rawg_info["name"]
    released = rawg_info["released"]
    if hltb_info is None:
        steam_id = 0
        dev = "-"
        avg_time = 0
    else:
        steam_id = hltb_info["profile_steam"]
        dev = hltb_info["profile_dev"]
        avg_time = hltb_info["comp_main"]
    if steam_id == 0:
        steam_id = ""
    if released is not None:
        release_date = datetime.datetime.strptime(released, "%Y-%m-%d")
    else:
        release_date = None
    genres = ""
    for genre in rawg_info["genres"]:
        genres += genre["name"] + ","
    genres = genres[:-1]
    image_url = rawg_info["background_image"]
    new_game = schemas.NewGame(
        # id=project_id,
        name=game_name,
        dev=dev,
        release_date=release_date,
        steam_id=str(steam_id),
        image_url=image_url,
        genres=genres,
        avg_time=avg_time,
        clockify_id=project_id,
        slug=rawg_info["slug"],
    )
    return new_game


async def sync_clockify_entries(
    db: Session, user: models.User, date: str = None, silent: bool = False
):
    try:
        total_entries = 0
        entries = clockify_api.get_time_entries(user.clockify_id, date)
        total_entries = len(entries)
        logger.info(
            "Sync " + str(total_entries) + " entries for user " + str(user.name)
        )
        if total_entries == 0:
            return 0
        await time_entries.sync_clockify_entries_db(db, user, entries, silent)
        return total_entries
    except Exception as e:
        logger.info("Error syncing clockify entries: " + str(e))
        raise e


def convert_blob_to_image(
    blob_data,
    output_format: str,
):
    try:
        image = Image.open(BytesIO(blob_data))
        converted_image = BytesIO()
        image.save(converted_image, format=output_format)
        converted_data = converted_image.getvalue()

        return converted_data
    except Exception as e:
        print(f"Error converting image: {e}")
        raise


async def send_message(msg, silent, image=None):
    logger.info("Sending message...")
    if not silent:
        bot = telegram.Bot(config.TELEGRAM_TOKEN)
        async with bot:
            try:
                if image is None:
                    await bot.send_message(
                        text=msg,
                        chat_id=config.TELEGRAM_GROUP_ID,
                        parse_mode=telegram.constants.ParseMode.MARKDOWN,
                    )
                else:
                    await bot.send_photo(
                        chat_id=config.TELEGRAM_GROUP_ID,
                        photo=image,
                        caption=msg,
                        parse_mode=telegram.constants.ParseMode.MARKDOWN,
                    )
                logger.info("Message sent successfully!")
            except Exception as e:
                logger.error("Error sending telegram message: " + str(e))


async def send_message_to_user(user_telegram_id, msg):
    logger.info("Sending message to user...")
    try:
        bot = telegram.Bot(config.TELEGRAM_TOKEN)
        async with bot:
            await bot.send_message(
                text=msg,
                chat_id=user_telegram_id,
                parse_mode=telegram.constants.ParseMode.MARKDOWN,
            )
        logger.info("Message sent successfully!")
    except Exception as e:
        logger.info(e)


async def send_message_to_admins(db: Session, msg):
    logger.info("Sending message to admins...")
    users_db = users.get_users(db)
    try:
        for user in users_db:
            if user.is_admin:
                bot = telegram.Bot(config.TELEGRAM_TOKEN)
                async with bot:
                    await bot.send_message(
                        text=msg,
                        chat_id=user.telegram_id,
                        parse_mode=telegram.constants.ParseMode.MARKDOWN,
                    )
                logger.info("Message sent successfully!")
    except Exception as e:
        logger.info(e)


def get_ach_message(
    ach: AchievementsElems, user: str, db: Session = None, game_id: str = None
):
    msg = "🏆"  +ach.value["title"]  +"🏆\n"
    if game_id is not None:
        game_db = games.get_game_by_id(db, game_id)
        msg = msg + ach.value["message"].format(user, game_db.name)
    else:
        msg = msg + ach.value["message"].format(user)
    return msg


def get_platforms(db: Session):
    try:
        stmt = select(
            models.PlatformTag.id,
            models.PlatformTag.name,
        )
        return db.execute(stmt).fetchall()
    except Exception as e:
        logger.info(e)
        raise e


def get_completed_tag(db: Session):
    try:
        stmt = select(
            models.OtherTag.id,
        ).where(models.OtherTag.name == "Completed")
        return db.execute(stmt).fetchone()
    except Exception as e:
        logger.info(e)
        raise e
