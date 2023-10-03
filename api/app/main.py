from typing import Union

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .config import Config
from .database import crud, models, schemas
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


######################
######## USER ########
######################


@app.get("/users/", tags=["Users"], response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    users = crud.get_users(db, skip, limit)
    return users


@app.get(
    "/users/{user_id}",
    tags=["Users"],
)
def get_user(user_id: Union[int, str], db: Session = Depends(get_db)):
    db_user = crud.get_user_by_tg_id(db, telegram_id=user_id)
    if db_user is None:
        db_user = crud.get_user_by_tg_username(db, telegram_username=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/", tags=["Users"], response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    db_user = crud.get_user_by_tg_username(db, username=user.username)
    # db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.put("/users/", tags=["Users"], response_model=schemas.User)
def update_user(user: schemas.User, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    return "TBI"


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@app.get(
    "/users/{user_id}/hours",
    tags=["Users"],
)
def user_played_hours(user_id: int, db: Session = Depends(get_db)):
    return "TBI"


@app.get("/users/{user}/games/played", tags=["Users"])
def user_games_played(
    user: Union[int, str],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    user_id = crud.get_user_id(db, user_id=user)
    played_games = crud.user_played_games(db, user_id)
    return played_games


@app.get("/users/{user_id}/games/played/most", tags=["Users"])
def user_games_played_most(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/users/{user_id}/games/played/last", tags=["Users"])
def user_games_played_last(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/users/{user_id}/games/completed", tags=["Users"])
def user_games_completed(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/users/{user_id}/streak/current", tags=["Users"])
def user_streak_current(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/users/{user_id}/streak/best", tags=["Users"])
def user_streak_best(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


#######################
######## GAMES ########
#######################


@app.get("/games/", tags=["Games"], response_model=list[schemas.GamesInfo])
def get_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    users = crud.get_games(db, skip, limit)
    return users


@app.get("/games/{name}", tags=["Games"], response_model=schemas.GamesInfo)
def get_game_by_name(name: str, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    game = crud.get_game_by_name(db, name)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not exists")

    return game


@app.post("/games/", tags=["Games"], response_model=schemas.GamesInfo)
def create_game(game: schemas.NewGame, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    db_game = crud.get_game_by_name(db, game.game)
    # db_user = crud.get_user_by_email(db, email=user.email)
    if db_game:
        raise HTTPException(status_code=400, detail="Email already registered")
    # return "Done"
    return crud.create_game(db=db, game=game)


##########################
######## RANKINGS ########
##########################

# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items


@app.get("/rankings/", tags=["Rankings"])
def rankings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/rankings/played-days", tags=["Rankings"])
def rankings_played_days(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/played-hours", tags=["Rankings"])
def rankings_played_hours(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/played-games", tags=["Rankings"])
def rankings_played_games(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/completed-games", tags=["Rankings"])
def rankings_completed_games(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/achievements", tags=["Rankings"])
def rankings_achievements(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/ratio", tags=["Rankings"])
def rankings_ratio(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return "TBI"


@app.get("/rankings/streak/current", tags=["Rankings"])
def rankings_streak_current(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/streak/best", tags=["Rankings"])
def rankings_streak_best(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/most-played-games", tags=["Rankings"])
def rankings_most_played_games(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/platform", tags=["Rankings"])
def rankings_platform(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return "TBI"


@app.get("/rankings/debt", tags=["Rankings"])
def rankings_debt(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return "TBI"


@app.get("/rankings/last-played-games", tags=["Rankings"])
def rankings_days(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    last_played = actions.get_last_played_games(db)
    return last_played


##############################
######## ACHIEVEMENTS ########
##############################


@app.get("/achievements", tags=["Achievements"])
def get_achievements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return "TBI"


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


@app.get("/sync-data", tags=["Actions"])
async def sync_data(date: str = None, db: Session = Depends(get_db)):
    try:
        await actions.sync_data(db, date)
        # actions.sync_clockify_entries(db, date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Sync completed!"


@app.get("/init-data", tags=["Actions"])
async def sync_data(db: Session = Depends(get_db)):
    try:
        await actions.init_data(db)
        # actions.sync_clockify_entries(db, date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Init completed!"
