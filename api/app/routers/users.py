from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import auth
from ..crud import games, users
from ..database import models, schemas
from ..database.database import SessionLocal, engine
from ..utils import actions as actions
from ..utils import logger as logger
from ..utils import my_utils as utils

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
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


class RankingUsersTypes(str, Enum):
    games = "games"


@router.get("/", response_model=list[schemas.User])
@version(1)
def get_users(db: Session = Depends(get_db)):
    """
    Get all users
    """
    users_db = users.get_users(db)
    return users_db


@router.get("/{username}", response_model=schemas.User)
@version(1)
def get_user(username: str, db: Session = Depends(get_db)):
    """
    Get user by Telegram username
    """
    user_db = users.get_user(db, username)
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db


@router.post("/", response_model=schemas.User)
@version(1)
def add_user(user: schemas.UserAddOrUpdate, db: Session = Depends(get_db)):
    """
    Add user
    """
    db_user = users.get_user(db, user.telegram_username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return users.create_user(db=db, user=user)


@router.put("/", response_model=schemas.User)
@version(1)
def update_user(user: schemas.UserAddOrUpdate, db: Session = Depends(get_db)):
    """
    Update user
    """
    db_user = users.get_user(db, user.telegram_username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not exists")
    return users.update_user(db=db, user=user)


@router.post("/{username}/new_game", response_model=schemas.UsersGames)
@version(1)
def add_game_to_user(
    username: str, game: schemas.NewGameUser, db: Session = Depends(get_db)
):
    """
    Add new game to user
    """
    user = users.get_user(db, username)
    played_games = users.get_games(db, user.id)
    for played_game in played_games:
        if played_game.game == game.game:
            raise HTTPException(status_code=400, detail="Game already exists")
    # TODO: Revise this exception and response codes
    try:
        return users.add_new_game(db=db, game=game, user=user)
    except Exception:
        raise HTTPException(status_code=500, detail="Error adding new game user")


@router.get(
    "/{username}/games",
    response_model=list[schemas.UsersGames],
)
@version(1)
def user_games(
    username: str,
    limit: int = None,
    completed: bool = None,
    db: Session = Depends(get_db),
):
    user_id = users.get_user(db, username=username).id
    played_games = users.get_games(db, user_id, limit, completed)
    return played_games


@router.put("/{username}/complete-game", response_model=schemas.CompletedGame)
@version(1)
async def complete_game(username: str, game_name: str, db: Session = Depends(get_db)):
    """
    Complete game by username
    """
    user_game = users.get_game(db, users.get_user(db, username).id, game_name)
    if user_game is None:
        raise HTTPException(status_code=404, detail="User is not playing this game")
    if user_game.completed == 1:
        raise HTTPException(status_code=409, detail="Game is already completed")
    num_completed_games, completion_time = users.complete_game(
        db, users.get_user(db, username).id, game_name
    )
    game_info = await utils.get_game_info(game_name)
    avg_time = game_info["hltb"]["comp_main"]
    games.update_avg_time_game(db, game_name, avg_time)
    return {
        "completed_games": num_completed_games,
        "completion_time": completion_time,
        "avg_time": avg_time,
    }


# @router.get("/{username}/{ranking}")
# @version(1)
# def user_rankings(
#     username: str,
#     ranking: RankingUsersTypes,
#     db: Session = Depends(get_db),
# ):
#     user_id = users.get_user(db, username=username).id
#     return user_id
