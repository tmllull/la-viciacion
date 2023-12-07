from fastapi import APIRouter, Depends, Header, HTTPException, Query, Security, status
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import auth
from ..config import Config
from ..crud import achievements, users
from ..database import models, schemas
from ..database.database import SessionLocal, engine
from ..utils import actions as actions
from ..utils import logger as logger
from ..utils import messages as msg

models.Base.metadata.create_all(bind=engine)

config = Config()

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
@version(1)
def test_endpoint(user: models.User = Security(auth.get_current_active_user)):
    """
    Test endpoint
    """
    if not user.is_admin:
        raise HTTPException(status_code=403, detail=msg.USER_NOT_ADMIN)
    return "Gratz! You are an admin."


@router.get("/init")
@version(1)
def init(
    db: Session = Depends(get_db),
    api_key: None = Security(auth.get_api_key),
):
    """
    Init base data
    """
    try:
        for admin in config.ADMIN_USERS:
            users.create_admin_user(db, admin)
        achievements.populate_achievements(db)
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


@router.put("/update_user", response_model=schemas.User)
@version(1)
def update_user(
    user_data: schemas.UserUpdate,
    user: models.User = Security(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update user by admin
    """
    if not user.is_admin:
        raise HTTPException(status_code=403, detail=msg.USER_NOT_ADMIN)
    db_user = users.get_user_by_username(db, user_data.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail=msg.USER_NOT_EXISTS)
    return users.update_user(db=db, user=user_data)


@router.get("/activate/{username}")
@version(1)
def activate_account(
    username: str,
    db: Session = Depends(get_db),
    api_key: None = Security(auth.get_api_key),
):
    if users.activate_account(db, username):
        return msg.ACCOUNT_ALREADY_ACTIVATED
    else:
        raise HTTPException(status_code=409, detail=msg.ACCOUNT_ALREADY_ACTIVATED)
