from fastapi import APIRouter, Depends, HTTPException, Query, Security
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import auth
from ..config import Config
from ..crud import users
from ..database import models
from ..database.database import SessionLocal, engine
from ..utils import actions as actions
from ..utils import logger as logger

models.Base.metadata.create_all(bind=engine)

config = Config()

router = APIRouter(
    tags=["Basic"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(auth.get_api_key)],
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


@router.get("/sync-data")
@version(1)
async def sync_data(
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
