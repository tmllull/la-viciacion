import re

from sqlalchemy.orm import Session

from ..database import crud
from . import logger
from .clockify_api import ClockifyApi

clockify = ClockifyApi()


def sync_clockify_entries(db: Session, date: str = None):
    users = crud.get_users(db)
    if date is None:
        logger.info("Syncing last time entries...")
    else:
        logger.info("Syncing time entries from " + date + "...")
    try:
        for user in users:
            entries = clockify.get_time_entries(user.clockify_id, date)
            crud.sync_clockify_entries(db, user.id, entries)
    except Exception as e:
        logger.info("Error syncing clockify entries: " + str(e))
        raise e


def convert_clockify_duration(duration):
    match = re.match(r"PT(\d+H)?(\d+M)?", duration)
    if match:
        horas_str = match.group(1)
        minutos_str = match.group(2)

        horas = int(horas_str[:-1]) if horas_str else 0
        minutos = int(minutos_str[:-1]) if minutos_str else 0

        # Convertir horas y minutos a segundos
        segundos = horas * 3600 + minutos * 60

        return segundos
    else:
        return 0
