from fastapi import APIRouter, Depends, HTTPException
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import auth
from ..crud import games, time_entries, users
from ..crud.achievements import Achievements
from ..database import models, schemas
from ..database.database import SessionLocal, engine
from ..utils import actions as actions
from ..utils import logger as logger
from ..utils import messages as msg
from ..utils import my_utils as utils

models.Base.metadata.create_all(bind=engine)

achievements = Achievements()

router = APIRouter(
    prefix="/utils",
    tags=["Utils"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(auth.get_current_active_user)],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/platforms")
@version(1)
def platforms(
    db: Session = Depends(get_db),
):
    """ """
    tags = utils.get_platforms(db)
    response = []
    for tag in tags:
        response.append({"id": tag[0], "name": tag[1]})
    return response


@router.get("/achievements")
@version(1)
def achievements_list(
    db: Session = Depends(get_db),
):
    """ """
    ach_list = achievements.get_achievements_list(db)
    response = []
    for ach in ach_list:
        response.append(ach.title)
    return response


@router.get("/playing")
@version(1)
def get_playing_users(db: Session = Depends(get_db)):
    """
    Get all users
    """
    users_db = users.get_users(db)
    playing = []
    for user in users_db:
        info = {}
        active_timer = time_entries.get_active_time_entry_by_user(db, user)
        if active_timer is not None:
            logger.info(active_timer)
            info["user"] = user.name
            info["game"] = games.get_game_by_id(
                db, active_timer.project_clockify_id
            ).name
            info["time"] = active_timer.start
            playing.append(info)
    return playing
