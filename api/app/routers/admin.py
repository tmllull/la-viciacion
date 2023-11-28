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
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(auth.get_api_key)],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    # user: None = Security(auth.get_current_active_user),
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


@router.put("/update_user", response_model=schemas.User)
@version(1)
def update_user(
    user_data: schemas.UserUpdate,
    # api_key: None = Security(auth.get_api_key),
    user: None = Security(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update user by admin
    """
    db_user = users.get_user_by_username(db, user_data.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not exists")
    return users.update_user(db=db, user=user_data)
