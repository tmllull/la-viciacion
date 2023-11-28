from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Security, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import auth
from ..config import Config
from ..crud import users
from ..database import models, schemas
from ..database.database import SessionLocal, engine
from ..utils import actions as actions
from ..utils import logger as logger

models.Base.metadata.create_all(bind=engine)

config = Config()

router = APIRouter(
    tags=["Basic"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(auth.get_api_key)],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
@version(1)
def hello_world():
    """
    Test endpoint
    """
    return "Hello world!"


@router.get("/init")
@version(1)
def init(db: Session = Depends(get_db)):
    """
    Init base data
    """
    try:
        for admin in config.ADMIN_USERS:
            users.create_admin_user(db, admin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return "Init completed!"


@router.get("/sync-data")
@version(1)
async def sync_data(
    api_key: None = Security(auth.get_api_key),
    start_date: str = Query(
        default=None,
        title="Start date",
        description="Start date to sync data from clockify time entries",
    ),
    silent: bool = Query(
        default=False,
        title="Run in silent mode",
        description="If True, notification will be disabled",
    ),
    sync_all: bool = Query(
        default=False,
        title="Sync all data",
        description="If True, all data from 'START_DATE' defined on .env will be retrieved",
    ),
    db: Session = Depends(get_db),
):
    try:
        for admin in config.ADMIN_USERS:
            users.create_admin_user(db, admin)
        await actions.sync_data(db, start_date, silent, sync_all)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Sync completed!"


# @router.get("/login")
# @version(1)
# def login():
#     """
#     Test endpoint
#     """
#     return "Hello world!"


@router.post("/register")
@version(1)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.invitation_key != config.INVITATION_KEY:
        raise HTTPException(status_code=400, detail="Invalid invitation key")
    db_user = users.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return users.create_user(db=db, user=user)


@router.post("/login", response_model=auth.Token)
@version(1)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(config.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = auth.create_access_token(
        data={"username": user.username, "is_admin": user.is_admin},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
