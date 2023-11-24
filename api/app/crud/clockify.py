import requests
from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ..config import Config
from ..crud import users
from ..database import models
from ..utils import actions as actions
from ..utils import logger
from ..utils import my_utils as utils
from ..utils.clockify_api import ClockifyApi

clockify = ClockifyApi()
config = Config()


def sync_clockify_tags(db: Session):
    tags = clockify.get_tags()
    for tag in tags:
        try:
            new_tag = models.ClockifyTags(id=tag["id"], name=tag["name"])
            db.add(new_tag)
            db.commit()
        except Exception:
            db.rollback()


def get_tag_id(db, tag_id):
    return (
        db.query(models.ClockifyTags.name)
        .filter(models.ClockifyTags.id == tag_id)
        .first()
    )
