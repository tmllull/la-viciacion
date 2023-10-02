from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .config import Config
from .database import crud, models, schemas
from .database.database import SessionLocal, engine
from .utils import actions as actions

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
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    users = crud.get_users(db, skip, limit)
    return users


@app.get(
    "/users/{user_id}",
    tags=["Users"],
)
def user_played_hours(user_id: int, db: Session = Depends(get_db)):
    return "TBI"


@app.get("/users/{telegram_id}", tags=["Users"], response_model=schemas.User)
def read_user(telegram_username: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_tg_username(db, telegram_username=telegram_username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/{telegram_username}", tags=["Users"], response_model=schemas.User)
def read_user(telegram_username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_tg_username(db, telegram_username=telegram_username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get(
    "/users/{name}",
    tags=["Users"],
)
def user_played_hours(name: int, db: Session = Depends(get_db)):
    return "TBI"


@app.post("/users/", tags=["Users"], response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    TODO: Add description
    """
    db_user = crud.get_user_by_tg_username(db, username=user.username)
    # db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.put("/users/", tags=["Users"], response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
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


@app.get("/users/{user_id}/games/played", tags=["Users"])
def user_games_played(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


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
def rankings_days(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return "TBI"


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
def sync_data(date: str = None, db: Session = Depends(get_db)):
    try:
        actions.sync_data(db, date)
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
