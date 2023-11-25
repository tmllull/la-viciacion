from fastapi import APIRouter, Depends, HTTPException
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import auth
from ..crud import games
from ..database import models, schemas
from ..database.database import SessionLocal, engine
from ..utils import actions as actions
from ..utils import logger as logger
from ..utils import my_utils as utils

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/games",
    tags=["Games"],
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


@router.get("/", response_model=list[schemas.GamesInfo])
@version(1)
def get_games(name: str = None, db: Session = Depends(get_db)):
    """
    Get all games from DB
    """
    logger.info("Getting games...")
    if name is None:
        games_db = games.get_games(db)
    else:
        games_db = games.get_game_by_name(db, name)
    return games_db


@router.get("/{game_id}", response_model=schemas.GamesInfo)
@version(1)
async def get_game_by_id(game_id: int, db: Session = Depends(get_db)):
    """
    Get game from DB by id
    """
    game_db = games.get_game_by_id(db, game_id)
    if game_db is None:
        raise HTTPException(status_code=404, detail="Game not exists")

    return game_db


# @router.get("/games/name/{name}", tags=["Games"], response_model=schemas.GamesInfo)
# @version(1)
# async def get_game_by_name(name: str, db: Session = Depends(get_db)):
#     """
#     Get game from DB by name
#     """
#     game_db = games.get_game_by_name(db, name)
#     if game_db is None:
#         raise HTTPException(status_code=404, detail="Game not exists")

#     return game_db


@router.get("/rawg/{name}")
@version(1)
async def get_game_rawg_by_name(name: str, db: Session = Depends(get_db)):
    """
    Get game info from RAWG and HLTB (not from DB)
    """
    game_info = await utils.get_game_info(name)
    return game_info


@router.post("/", response_model=schemas.GamesInfo, status_code=201)
@version(1)
def create_game(game: schemas.NewGame, db: Session = Depends(get_db)):
    """
    Create new game
    """
    if games.get_game_by_name(db, game.name):
        raise HTTPException(status_code=400, detail="Game already in DB")
    return games.new_game(db=db, game=game)
