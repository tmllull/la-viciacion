from enum import Enum

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import auth
from ..crud import rankings
from ..database import models
from ..database.database import SessionLocal, engine
from ..utils import actions as actions
from ..utils import logger as logger

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(auth.get_api_key)],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RankingStatisticsTypes(str, Enum):
    hours = "hours"
    days = "days"


class UserStatisticsTypes(str, Enum):
    hours = "hours"
    days = "days"


@router.get("/rankings")
@version(1)
def get_ranking_statistics(
    ranking: RankingStatisticsTypes,
    db: Session = Depends(get_db),
):
    if ranking == "hours":
        return rankings.get_current_ranking_hours_players(db)
    elif ranking == "days":
        return rankings.get_current_ranking_days_players(db)
    else:
        return {"message": "More rankings are coming"}


@router.get("/users")
@version(1)
def get_user_statistics(
    ranking: UserStatisticsTypes,
    db: Session = Depends(get_db),
):
    return {"message": "TBI"}


# @router.get("/rankings/played-hours", tags=["Rankings"])
# def rankings_played_hours(db: Session = Depends(get_db)):
#     return rankings.get_current_ranking_hours_players(db)


# @router.get("/rankings/played-days", tags=["Rankings"])
# def rankings_played_days(db: Session = Depends(get_db)):
#     return rankings.get_current_ranking_days_players(db)
