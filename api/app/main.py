from typing import Union

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .config import Config
from .database import models, schemas
from .database.crud import games, users
from .database.database import SessionLocal, engine
from .utils import actions as actions
from .utils import logger as logger

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


# @app.get("/init-data")
# async def sync_data(db: Session = Depends(get_db)):
#     try:
#         await actions.init_data(db)
#         # actions.sync_clockify_entries(db, date)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     return "Init completed!"


@app.get("/sync-data")
async def sync_data(
    start_date: str = None, silent: bool = False, db: Session = Depends(get_db)
):
    try:
        await actions.sync_data(db, start_date, silent)
        # actions.sync_clockify_entries(db, date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Sync completed!"


######################
######## USER ########
######################


@app.get("/users/", tags=["Users"], response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    users_db = users.get_users(db)
    return users_db


@app.get("/users/{user}", tags=["Users"])
def get_user(user: Union[int, str], db: Session = Depends(get_db)):
    user_db = users.get_user(db, user=user)
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db


# @app.post("/users/", tags=["Users"], response_model=schemas.User)
# def create_user(user: schemas.User, db: Session = Depends(get_db)):
#     """
#     TODO: Add description
#     """
#     db_user = crud.get_user(db, user=user.username)
#     # db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.put("/users/", tags=["Users"], response_model=schemas.User)
# def update_user(user: schemas.User, db: Session = Depends(get_db)):
#     """
#     TODO: Add description
#     """
#     return "TBI"


@app.post("/users/{user}/new_game", tags=["Users"])
def add_game(
    user: Union[str, int], game: schemas.NewGameUser, db: Session = Depends(get_db)
):
    """
    TODO: Add description
    """
    user_id = users.get_user(db, user).id
    played_games = users.get_games(db, user_id)
    for played_game in played_games:
        if played_game.game == game.game:
            raise HTTPException(status_code=400, detail="Game already exists")

    try:
        users.add_new_game(db=db, game=game, user_id=user_id)
    except:
        raise HTTPException(status_code=500, detail="Error adding new game user")


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.get(
#     "/users/{user_id}/hours",
#     tags=["Users"],
# )
# def user_played_hours(user_id: int, db: Session = Depends(get_db)):
#     return "TBI"


@app.get(
    "/users/{user}/games/played",
    tags=["Users"],
    response_model=list[schemas.UsersGames],
)
def user_games_played(
    user: Union[int, str],
    limit: int = None,
    completed: bool = None,
    db: Session = Depends(get_db),
):
    user_id = users.get_user(db, user=user).id
    played_games = users.get_games(db, user_id, limit, completed)
    return played_games


@app.put("/users/{user}/complete-game", tags=["Users"])
async def complete_game(user: str, game_name: str, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    num_completed_games = users.complete_game(
        db, users.get_user(db, user).id, game_name
    )
    game_info = await actions.get_game_info(game_name)
    avg_time = game_info["hltb"]["comp_main"]
    games.update_avg_time_game(db, game_name, avg_time)
    return {"completed_games": num_completed_games, "avg_time": avg_time}


# @app.get("/users/{user_id}/games/played/most", tags=["Users"])
# def user_games_played_most(
#     user_id: int,  limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.get("/users/{user_id}/games/played/last", tags=["Users"])
# def user_games_played_last(
#     user_id: int,  limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.get("/users/{user_id}/games/completed", tags=["Users"])
# def user_games_completed(
#     user_id: int,  limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.get("/users/{user_id}/streak/current", tags=["Users"])
# def user_streak_current(
#     user_id: int,  limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.get("/users/{user_id}/streak/best", tags=["Users"])
# def user_streak_best(
#     user_id: int,  limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


#######################
######## GAMES ########
#######################


@app.get("/games/", tags=["Games"], response_model=list[schemas.GamesInfo])
def get_games(limit: int = 10000, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    games_db = games.get_games(db, limit)
    return games_db


@app.get("/games/{name}", tags=["Games"], response_model=schemas.GamesInfo)
async def get_game_by_name(name: str, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    # await actions.search_game_info_by_name(name)
    game_db = games.get_game_by_name(db, name)
    if game_db is None:
        raise HTTPException(status_code=404, detail="Game not exists")

    return game_db


@app.get("/games/rawg/{name}", tags=["Games"])
async def get_game_rawg_by_name(name: str, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    # await actions.search_game_info_by_name(name)
    game_info = await actions.get_game_info(name)
    return game_info


@app.post("/games/", tags=["Games"], response_model=schemas.GamesInfo)
def create_game(game: schemas.NewGame, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    if games.get_game_by_name(db, game.name):
        raise HTTPException(status_code=400, detail="Game already in DB")
    return games.new_game(db=db, game=game)


##########################
######## RANKINGS ########
##########################

# @app.get("/items/", response_model=list[schemas.Item])
# def read_items( limit: int = 10000, db: Session = Depends(get_db)):
#     items = crud.get_items(db,  limit=limit)
#     return items


# @app.get("/rankings/", tags=["Rankings"])
# def rankings( limit: int = 10000, db: Session = Depends(get_db)):
#     items = crud.get_items(db,  limit=limit)
#     return items


# @app.get("/rankings/played-days", tags=["Rankings"])
# def rankings_played_days(
#      limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.get("/rankings/played-hours", tags=["Rankings"])
# def rankings_played_hours(
#      limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.get("/rankings/played-games", tags=["Rankings"])
# def rankings_played_games(
#      limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.get("/rankings/completed-games", tags=["Rankings"])
# def rankings_completed_games(
#      limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.get("/rankings/achievements", tags=["Rankings"])
# def rankings_achievements(
#      limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.get("/rankings/ratio", tags=["Rankings"])
# def rankings_ratio( limit: int = 10000, db: Session = Depends(get_db)):
#     return "TBI"


# @app.get("/rankings/streak/current", tags=["Rankings"])
# def rankings_streak_current(
#      limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.get("/rankings/streak/best", tags=["Rankings"])
# def rankings_streak_best(
#      limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.get("/rankings/most-played-games", tags=["Rankings"])
# def rankings_most_played_games(
#      limit: int = 10000, db: Session = Depends(get_db)
# ):
#     return "TBI"


# @app.get("/rankings/platform", tags=["Rankings"])
# def rankings_platform( limit: int = 10000, db: Session = Depends(get_db)):
#     return "TBI"


# @app.get("/rankings/debt", tags=["Rankings"])
# def rankings_debt( limit: int = 10000, db: Session = Depends(get_db)):
#     return "TBI"


# @app.get("/rankings/last-played-games", tags=["Rankings"])
# def rankings_days( limit: int = 10, db: Session = Depends(get_db)):
#     last_played = actions.get_last_played_games(db)
#     return last_played


##############################
######## ACHIEVEMENTS ########
##############################


# @app.get("/achievements", tags=["Achievements"])
# def get_achievements( limit: int = 10000, db: Session = Depends(get_db)):
#     return "TBI"


# @app.post("/users/")
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)

#########################
######## ACTIONS ########
#########################
