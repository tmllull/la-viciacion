from enum import Enum

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import auth
from ..crud import rankings
from ..database import models, schemas
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


@router.get(
    "/rankings",
    # response_model=list[schemas.RankingsResponse],
    response_description="Return a list of rankings",
)
@version(1)
def get_ranking_statistics(
    ranking: str = None,
    db: Session = Depends(get_db),
):
    """
    Get general rankings. To retrieve only specific rankings, add 'ranking' param with desired rankings, separated by comma (,).

    Allowed values: 'hours', 'days', 'user_played_games',
    'completed_games', 'achievements', 'ratio', 'current_streak',
    'best_streak', 'most_played_games', 'platform_played', 'debt', 'last_played'
    """
    if ranking is not None:
        rankings_list = ranking.split(",")
    else:
        rankings_list = [elem.value for elem in RankingStatisticsTypes]
    response = []
    for ranking_type in rankings_list:
        content = {}
        if ranking_type == RankingStatisticsTypes.hours:
            data = rankings.user_hours_players(db)
        elif ranking_type == RankingStatisticsTypes.days:
            data = rankings.user_days_players(db)
        elif ranking_type == RankingStatisticsTypes.user_played_games:
            data = rankings.user_played_games(db)
        elif ranking_type == RankingStatisticsTypes.completed_games:
            data = rankings.user_completed_games(db)
        elif ranking_type == RankingStatisticsTypes.achievements:
            data = [{"message": "Achievements is nos implemented yet"}]
        elif ranking_type == RankingStatisticsTypes.ratio:
            data = [{"message": "Ratio is nos implemented yet"}]
        elif ranking_type == RankingStatisticsTypes.current_streak:
            data = rankings.user_current_streak(db)
        elif ranking_type == RankingStatisticsTypes.best_streak:
            data = rankings.user_best_streak(db)
        elif ranking_type == RankingStatisticsTypes.most_played_games:
            data = rankings.games_most_played(db)
        elif ranking_type == RankingStatisticsTypes.platform_played:
            data = rankings.platform_played_games(db)
        elif ranking_type == RankingStatisticsTypes.debt:
            data = [{"message": "Debt is nos implemented yet"}]
        elif ranking_type == RankingStatisticsTypes.last_played:
            data = rankings.games_last_played(db)
        else:
            data = {"message": "More rankings are coming"}
        content["type"] = ranking_type
        content["data"] = data
        response.append(content)
    return response


@router.get("/users")
@version(1)
def get_user_statistics(
    ranking: str = None,
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
