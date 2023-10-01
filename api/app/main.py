from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import crud, models, schemas
from .database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def hello_world():
    return "Hello world!"


######################
######## USER ########
######################


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@app.get("/users/{telegram_username}", response_model=schemas.User)
def read_user(telegram_username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_tg_username(db, telegram_username=telegram_username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/{telegram_id}", response_model=schemas.User)
def read_user(telegram_username: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_tg_username(db, telegram_username=telegram_username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/{user_id}/hours")
def user_played_hours(user_id: int, db: Session = Depends(get_db)):
    return "TBI"


@app.get("/users/{user_id}/games/played")
def user_games_played(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/users/{user_id}/games/played/most")
def user_games_played_most(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/users/{user_id}/games/played/last")
def user_games_played_last(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/users/{user_id}/games/completed")
def user_games_completed(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/users/{user_id}/streak/current")
def user_streak_current(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/users/{user_id}/streak/best")
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


@app.get("/rankings/")
def rankings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/rankings/played_days")
def rankings_played_days(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/played_hours")
def rankings_played_hours(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/played_games")
def rankings_played_games(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/completed_games")
def rankings_completed_games(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/achievements")
def rankings_achievements(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/ratio")
def rankings_ratio(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return "TBI"


@app.get("/rankings/streak/current")
def rankings_streak_current(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/streak/best")
def rankings_streak_best(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/most_played_games")
def rankings_most_played_games(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return "TBI"


@app.get("/rankings/platform")
def rankings_platform(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return "TBI"


@app.get("/rankings/debt")
def rankings_debt(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return "TBI"


@app.get("/rankings/last_played_games")
def rankings_days(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return "TBI"


##############################
######## ACHIEVEMENTS ########
##############################


@app.get("/achievements")
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
