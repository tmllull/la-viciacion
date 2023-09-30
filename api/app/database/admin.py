from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ..utils import logger
from . import models, schemas


def get_users(db: Session):
    """Get all users

    Returns:
        list: A list of users
    """
    return db.query(models.User)
