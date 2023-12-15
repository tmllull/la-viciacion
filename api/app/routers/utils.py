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
    prefix="/utils",
    tags=["Utils"],
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


@router.get("/platforms")
@version(1)
def platforms(
    db: Session = Depends(get_db),
):
    """ """
    tags = utils.get_platforms(db)
    response = []
    for tag in tags:
        response.append({"id": tag[0], "name": tag[1]})
    return response
