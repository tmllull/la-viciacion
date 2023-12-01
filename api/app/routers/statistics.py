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
    dependencies=[Depends(auth.get_current_active_user)],
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
    user_played_games = "user_played_games"
    completed_games = "completed_games"
    achievements = "achievements"
    ratio = "ratio"
    current_streak = "current_streak"
    best_streak = "best_streak"
    most_played_games = "most_played_games"
    platform_played = "platform_played"
    debt = "debt"
    last_played = "last_played"


class UserStatisticsTypes(str, Enum):
    played_games = "played_games"
    completed_games = "completed_games"
    top_games = "top_games"
    achievements = "achievements"
    streak = "streak"


@router.get("/rankings")
@version(1)
def get_ranking_statistics(
    ranking: RankingStatisticsTypes,
    db: Session = Depends(get_db),
):
    if ranking == RankingStatisticsTypes.hours:
        return rankings.user_hours_players(db)
    elif ranking == RankingStatisticsTypes.days:
        return rankings.user_days_players(db)
    elif ranking == RankingStatisticsTypes.user_played_games:
        return rankings.user_played_games(db)
    elif ranking == RankingStatisticsTypes.completed_games:
        return rankings.user_completed_games(db)
    elif ranking == RankingStatisticsTypes.achievements:
        return {"message": "TBI"}
    elif ranking == RankingStatisticsTypes.ratio:
        return {"message": "TBI"}
    elif ranking == RankingStatisticsTypes.current_streak:
        return rankings.user_current_streak(db)
    elif ranking == RankingStatisticsTypes.best_streak:
        return rankings.user_best_streak(db)
    elif ranking == RankingStatisticsTypes.most_played_games:
        return rankings.games_most_played(db)
    elif ranking == RankingStatisticsTypes.platform_played:
        return rankings.platform_played_games(db)
    elif ranking == RankingStatisticsTypes.debt:
        return {"message": "TBI"}
    elif ranking == RankingStatisticsTypes.last_played:
        return rankings.games_last_played(db)
    else:
        return {"message": "More rankings are coming"}


@router.get("/users")
@version(1)
def get_user_statistics(
    ranking: UserStatisticsTypes,
    db: Session = Depends(get_db),
):
    if ranking == UserStatisticsTypes.played_games:
        return {"message": "TBI"}
    if ranking == UserStatisticsTypes.completed_games:
        return {"message": "TBI"}
    if ranking == UserStatisticsTypes.top_games:
        return {"message": "TBI"}
    if ranking == UserStatisticsTypes.achievements:
        return {"message": "TBI"}
    if ranking == UserStatisticsTypes.streak:
        return {"message": "TBI"}
    return {"message": "TBI"}
