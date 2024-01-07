from enum import Enum
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import auth
from ..crud import users as users_crud
from ..database import models, schemas
from ..database.database import SessionLocal, engine
from ..routers import admin, games, statistics, users, utils
from ..utils import actions as actions
from ..utils import logger as logger

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/bot",
    tags=["Bot"],
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


#################
##### USERS #####
#################


@router.get("/users/{username}", response_model=schemas.User)
@version(1)
def get_user(username: str, db: Session = Depends(get_db)):
    """
    Get user by username
    """
    return users.get_user(username, db)


@router.put("/users", response_model=schemas.User)
@version(1)
def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Update user
    """
    return users.update_user(user, db)


@router.patch("/users", response_model=schemas.User)
@version(1)
def update_user(user: schemas.TelegramUser, db: Session = Depends(get_db)):
    """
    Update user Telegram ID
    """
    return users_crud.update_user_telegram_id(db, user)


@router.post("/users/{username}/new_game", response_model=schemas.UserGame)
@version(1)
async def add_game_to_user(
    username: str, game: schemas.NewGameUser, db: Session = Depends(get_db)
):
    """
    Add new game to user list
    """
    return await users.add_game_to_user(username, game, db)


@router.get(
    "/users/{username}/games",
    response_model=list[schemas.UserGame],
)
@version(1)
def user_games(
    username: str,
    limit: int = None,
    completed: bool = None,
    db: Session = Depends(get_db),
):
    return users.get_games(username, limit, completed, db)


@router.patch("/users/{username}/complete-game")
@version(1)
async def complete_game(username: str, game_id: str, db: Session = Depends(get_db)):
    """
    Complete game
    """
    return await users.complete_game(username, game_id, db)


@router.patch("/users/{username}/rate-game")
@version(1)
async def rate_game(
    username: str, game_id: str, score: float, db: Session = Depends(get_db)
):
    """
    Rate game
    """
    return await users.rate_game(username, game_id, score, db)


#################
##### GAMES #####
#################


@router.get("/games", response_model=list[schemas.Game])
@version(1)
def get_games(name: str = None, limit: int = None, db: Session = Depends(get_db)):
    """
    Get games from DB
    """
    return games.get_games(name, limit, db)


@router.get("/games/{game_id}", response_model=schemas.Game)
@version(1)
async def get_game_by_id(game_id: str, db: Session = Depends(get_db)):
    """
    Get game from DB by id
    """
    return await games.get_game_by_id(game_id=game_id, db=db)


@router.post("/games", response_model=schemas.Game, status_code=201)
@version(1)
async def create_game(game: schemas.NewGame, db: Session = Depends(get_db)):
    """
    Create new game
    """
    return await games.create_game(game, db)


@router.get("/games/rawg/{name}")
@version(1)
async def get_game_rawg_by_name(name: str, db: Session = Depends(get_db)):
    """
    Get game info from RAWG and HLTB (not from DB)
    """
    return await games.get_game_rawg_by_name(name, db)


######################
##### STATISTICS #####
######################


class RankingStatisticsTypes(str, Enum):
    user_hours = "user_hours"
    user_days = "user_days"
    user_played_games = "user_played_games"
    user_completed_games = "user_completed_games"
    achievements = "achievements"
    user_ratio = "user_ratio"
    user_current_streak = "user_current_streak"
    user_best_streak = "user_best_streak"
    games_most_played = "games_most_played"
    platform_played = "platform_played"
    debt = "debt"
    games_last_played = "games_last_played"


class UserStatisticsTypes(str, Enum):
    played_games = "played_games"
    completed_games = "completed_games"
    top_games = "top_games"
    achievements = "achievements"
    streak = "streak"


@router.get("/statistics/rankings")
@version(1)
def get_ranking_statistics(
    ranking: str,
    db: Session = Depends(get_db),
):
    return statistics.get_ranking_statistics(ranking, db)


@router.get("/statistics/users/{username}")
@version(1)
def get_user_statistics(
    ranking: UserStatisticsTypes,
    username: str,
    db: Session = Depends(get_db),
):
    return statistics.get_user_statistics(username, ranking, db)


#################
##### OTHER #####
#################


@router.get("/activate/{username}")
@version(1)
def get_user_statistics(
    username: str,
    db: Session = Depends(get_db),
):
    return admin.activate_account(username, db)


@router.get("/utils/platforms")
@version(1)
def platforms(
    db: Session = Depends(get_db),
):
    """ """
    return utils.platforms(db)


@router.get("/utils/achievements")
@version(1)
def achievements(
    db: Session = Depends(get_db),
):
    """ """
    return utils.achievements_list(db)


@router.get("/utils/playing")
@version(1)
def playing_users(db: Session = Depends(get_db)):
    """
    Get playing users
    """
    return utils.get_playing_users(db)
