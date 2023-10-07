from typing import Union

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .config import Config
from .database import models, schemas
from .database.crud import games, rankings, time_entries, users
from .database.database import SessionLocal, engine
from .utils import actions as actions
from .utils import logger as logger
from .utils import my_utils as utils

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
config = Config()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def hello_world():
    """
    Test endpoint
    """
    return "Hello world!"


@app.get("/sync-data")
async def sync_data(
    start_date: str = None,
    silent: bool = False,
    sync_all: bool = False,
    db: Session = Depends(get_db),
):
    try:
        for admin in config.ADMIN_USERS:
            users.create_admin_user(db, admin)
        await actions.sync_data(db, start_date, silent, sync_all)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Sync completed!"


######################
######## USER ########
######################


@app.get("/users", tags=["Users"], response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    """
    Get all users
    """
    users_db = users.get_users(db)
    return users_db


@app.post("/users/{username}", tags=["Users"], response_model=schemas.User)
def get_user(
    username: str, user: schemas.TelegramUser = None, db: Session = Depends(get_db)
):
    """
    Get user by Telegram username
    """
    user_db = users.get_user(db, username, user)
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db


# @app.post("/users", tags=["Users"], response_model=schemas.User)
# def create_user(user: schemas.User, db: Session = Depends(get_db)):
#     """
#     TODO: Add description
#     """
#     db_user = crud.get_user(db, user=user.username)
#     # db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


@app.post(
    "/users/{username}/new_game", tags=["Users"], response_model=schemas.UsersGames
)
def add_game(username: str, game: schemas.NewGameUser, db: Session = Depends(get_db)):
    """
    TODO: Add description
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


@app.get(
    "/users/{username}/games/played",
    tags=["Users"],
    response_model=list[schemas.UsersGames],
)
def user_games_played(
    username: str,
    limit: int = None,
    completed: bool = None,
    db: Session = Depends(get_db),
):
    user_id = users.get_user(db, username=username).id
    played_games = users.get_games(db, user_id, limit, completed)
    return played_games


@app.put(
    "/users/{user}/complete-game", tags=["Users"], response_model=schemas.UsersGames
)
async def complete_game(user: str, game_name: str, db: Session = Depends(get_db)):
    """
    Complete game by user
    """
    num_completed_games = users.complete_game(
        db, users.get_user(db, user).id, game_name
    )
    game_info = await utils.get_game_info(game_name)
    avg_time = game_info["hltb"]["comp_main"]
    games.update_avg_time_game(db, game_name, avg_time)
    return {"completed_games": num_completed_games, "avg_time": avg_time}


#######################
######## GAMES ########
#######################


@app.get("/games", tags=["Games"], response_model=list[schemas.GamesInfo])
def get_games(limit: int = 10000, db: Session = Depends(get_db)):
    """
    Get all games from DB
    """
    games_db = games.get_games(db, limit)
    return games_db


@app.get("/games/{name}", tags=["Games"], response_model=schemas.GamesInfo)
async def get_game_by_name(name: str, db: Session = Depends(get_db)):
    """
    Get game from DB by name
    """
    game_db = games.get_game_by_name(db, name)
    if game_db is None:
        raise HTTPException(status_code=404, detail="Game not exists")

    return game_db


@app.get("/games/rawg/{name}", tags=["Games"])
async def get_game_rawg_by_name(name: str, db: Session = Depends(get_db)):
    """
    Get game info from RAWG and HLTB (not from DB)
    """
    game_info = await utils.get_game_info(name)
    return game_info


@app.post("/games", tags=["Games"], response_model=schemas.GamesInfo, status_code=201)
def create_game(game: schemas.NewGame, db: Session = Depends(get_db)):
    """
    Create new game
    """
    if games.get_game_by_name(db, game.name):
        raise HTTPException(status_code=400, detail="Game already in DB")
    return games.new_game(db=db, game=game)


##########################
######## RANKINGS ########
##########################


@app.get("/rankings", tags=["Rankings"])
def rankings_played_hours(type: str = None, db: Session = Depends(get_db)):
    if type is None:
        return {"message": "Return all rankings TBI"}
    else:
        if type == "hours":
            return rankings.get_current_ranking_hours_players(db)
        elif type == "days":
            return rankings.get_current_ranking_days_players(db)
        else:
            return {"message": "More rankings in coming"}


# @app.get("/rankings/played-hours", tags=["Rankings"])
# def rankings_played_hours(db: Session = Depends(get_db)):
#     return rankings.get_current_ranking_hours_players(db)


# @app.get("/rankings/played-days", tags=["Rankings"])
# def rankings_played_days(db: Session = Depends(get_db)):
#     return rankings.get_current_ranking_days_players(db)
