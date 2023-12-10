import datetime
from enum import Enum

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    Response,
    Security,
    UploadFile,
)
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import auth
from ..crud import games, users
from ..database import models, schemas
from ..database.database import SessionLocal, engine
from ..utils import actions as actions
from ..utils import logger as logger
from ..utils import messages as msg
from ..utils import my_utils as utils

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
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
    Get user by username
    """
    user_db = users.get_user_by_username(db, username)
    if user_db is None:
        raise HTTPException(status_code=404, detail=msg.USER_NOT_EXISTS)
    return user_db


# @router.post("/", response_model=schemas.User)
# @version(1)
# def add_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
#     """
#     Add user
#     """
#     db_user = users.get_user_by_username(db, user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="User already registered")
#     return users.create_user(db=db, user=user)


@router.put("/", response_model=schemas.User)
@version(1)
def update_user(
    user: schemas.UserUpdate,
    active_user: models.User = Security(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update user
    """
    if active_user.username != user.username:
        raise HTTPException(status_code=403, detail=msg.USER_NOT_ADMIN)
    db_user = users.get_user_by_username(db, user.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail=msg.USER_NOT_EXISTS)
    return users.update_user(db=db, user=user)


@router.post("/{username}/new_game", response_model=schemas.UserGame)
@version(1)
async def add_game_to_user(
    username: str, game: schemas.NewGameUser, db: Session = Depends(get_db)
):
    """
    Add new game to user list
    """
    user = users.get_user_by_username(db, username)
    already_playing = users.get_game_by_clockify_id(
        db, user.id, game.project_clockify_id
    )
    if already_playing:
        raise HTTPException(status_code=409, detail=msg.USER_ALREADY_PLAYING)
    # played_games = users.get_games(db, user.id)
    # for played_game in played_games:
    #     if played_game.project_clockify_id == game.project_clockify_id:
    #         raise HTTPException(
    #             status_code=409, detail="User is already playing this game"
    #         )
    try:
        played_games = users.get_games(db, user.id)
        new_game = users.add_new_game(db=db, game=game, user=user)
        game_name = games.get_game_by_clockify_id(db, game.project_clockify_id).name
        total_games = played_games.count() + 1
        await utils.send_message(
            user.name
            + " acaba de empezar su juego número "
            + str(total_games)
            + ": *"
            + game_name
            + "*"
        )
        return new_game
    except Exception as e:
        logger.info(e)
        raise HTTPException(
            status_code=500, detail="Error adding new game user: " + str(e)
        )


@router.get(
    "/{username}/games",
    response_model=list[schemas.UserGame],
)
@version(1)
def get_games(
    username: str,
    limit: int = None,
    completed: bool = None,
    db: Session = Depends(get_db),
):
    user = users.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail=msg.USER_NOT_EXISTS)
    played_games = users.get_games(db, user.id, limit, completed)
    return played_games


@router.patch("/{username}/complete-game", response_model=schemas.CompletedGame)
@version(1)
async def complete_game(username: str, game_id: int, db: Session = Depends(get_db)):
    """
    Complete game by username
    """
    try:
        user = users.get_user_by_username(db, username)
        user_game = users.get_game_by_id(db, user.id, game_id)
        if user_game is None:
            raise HTTPException(status_code=404, detail=msg.USER_NOT_EXISTS)
        if user_game.completed == 1:
            raise HTTPException(status_code=409, detail=msg.GAME_ALREADY_COMPLETED)
        num_completed_games, completion_time = users.complete_game(db, user.id, game_id)
        db_game = games.get_game_by_id(db, game_id)
        game_info = await utils.get_game_info(db_game.name)
        avg_time = game_info["hltb"]["comp_main"]
        games.update_avg_time_game(db, game_id, avg_time)
        game = games.get_game_by_id(db, game_id)
        message = (
            user.name
            + " acaba de completar su juego número "
            + str(num_completed_games)
            + ": *"
            + game.name
            + "* en "
            + str(utils.convert_time_to_hours(completion_time))
            + ". La media está en "
            + str(utils.convert_time_to_hours(avg_time))
            + "."
        )
        logger.info(message)
        await utils.send_message(message)
        return {
            "completed_games": num_completed_games,
            "completion_time": completion_time,
            "avg_time": avg_time,
        }
    except Exception as e:
        logger.info(e)
        raise HTTPException(
            status_code=500, detail="Error completing game_user: " + str(e)
        )


@router.patch("/{username}/avatar")
@version(1)
async def upload_avatar(
    username: str,
    # file: Annotated[UploadFile, File(description="A file read as UploadFile")],
    file: UploadFile,
    db: Session = Depends(get_db),
):
    allowed_types = ["image/jpeg", "image/jpg", "image/png"]
    logger.info("Content Type: " + file.content_type)
    if file.content_type not in allowed_types:
        logger.info(msg.FILE_TYPE_NOT_ALLOWED)
        raise HTTPException(
            status_code=400,
            detail=msg.FILE_TYPE_NOT_ALLOWED,
        )
    if not users.get_user_by_username(db, username):
        logger.info(msg.USER_NOT_EXISTS)
        raise HTTPException(status_code=404, detail=msg.USER_NOT_EXISTS)
    logger.info("File size: " + str(file.size))
    if file.size > 2097152:
        logger.info(msg.FILE_TOO_BIG)
        raise HTTPException(status_code=400, detail=msg.FILE_TOO_BIG)
    try:
        data = await file.read()
        users.upload_avatar(db, username, data)
        return "Avatar uploaded"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{username}/avatar")
@version(1)
async def get_avatar(
    username: str,
    db: Session = Depends(get_db),
):
    if not users.get_user_by_username(db, username):
        logger.info(msg.USER_NOT_EXISTS)
        raise HTTPException(status_code=404, detail=msg.USER_NOT_EXISTS)
    try:
        data = users.get_avatar(db, username)
        return Response(content=data[0], media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
