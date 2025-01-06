import requests
from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ...config import Config
from . import users
from .. import models
from ...utils import actions as actions
from ...utils import my_utils as utils
from ...utils.clockify_api import ClockifyApi
from ...utils.logger import LogManager
from sqlalchemy.exc import SQLAlchemyError
from ..database import SessionLocal

db = SessionLocal()

log_manager = LogManager()
logger = log_manager.get_logger()

clockify = ClockifyApi()
config = Config()


def get_queue():
    try:
        return db.query(models.RequestSync).all()
    except SQLAlchemyError as e:
        logger.error("Error getting request queue: " + str(e))
        raise


def get_active_sync():
    try:
        db.refresh()
        return db.query(models.RequestSync).first()
    except SQLAlchemyError as e:
        logger.error("Error getting request queue: " + str(e))
        raise


def refresh_active_sync(process):
    db.refresh(process)


def add_request_to_queue(request_id: str):
    try:
        new_request = models.RequestSync(request_id=request_id)
        db.add(new_request)
        db.commit()
    except SQLAlchemyError as e:
        logger.error("Error adding request to queue: " + str(e))
        raise

    return True


def delete_request_from_queue(request_id: str):
    try:
        logger.debug("Deleting request from queue: " + request_id)
        db.query(models.RequestSync).filter(
            models.RequestSync.request_id == request_id
        ).delete()
        db.commit()
    except SQLAlchemyError as e:
        logger.error("Error deleting request from queue: " + str(e))
        raise

    return True
