from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    Query,
    Response,
    Security,
    UploadFile,
    status,
)
from fastapi_versioning import version
from sqlalchemy.orm import Session

from .. import auth
from ..config import Config
from ..crud import users
from ..crud.achievements import Achievements
from ..database import models, schemas
from ..database.database import SessionLocal, engine
from ..utils import actions as actions
from ..utils import logger as logger
from ..utils import messages as msg
from ..utils.email import Email

models.Base.metadata.create_all(bind=engine)

config = Config()
achievements = Achievements()
email = Email()

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
        logger.info("Creating admin users")
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
    sync_season: bool = Query(
        default=None,
        title="Sync all season data",
        description="Sync all time entries for the current year",
    ),
    silent: bool = Query(
        default=None,
        title="Run in silent mode",
        description="Disable Telegram notifications",
    ),
    sync_all: bool = Query(
        default=None,
        title="Sync all data",
        description="Sync all time entries for the whole time",
    ),
    db: Session = Depends(get_db),
):
    try:
        for admin in config.ADMIN_USERS:
            users.create_admin_user(db, admin)
        await actions.sync_data(
            db, sync_season=sync_season, silent=silent, sync_all=sync_all
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return "Sync completed!"


@router.put("/update_user", response_model=schemas.User)
@version(1)
def update_user(
    user_data: schemas.UserUpdateForAdmin,
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
    return users.update_user_as_admin(db=db, user=user_data)


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


@router.post("/send_email")
@version(1)
def send_email(
    info: schemas.Email,
    api_key: None = Security(auth.get_api_key),
):
    """ """
    return email.send_mail(
        receivers=info.receiver, subject=info.subject, msg=info.message
    )


# @router.patch("/achievement-image/{achievement}")
# @version(1)
# async def upload_achievement_image(
#     achievement: str,
#     # file: Annotated[UploadFile, File(description="A file read as UploadFile")],
#     file: UploadFile,
#     db: Session = Depends(get_db),
#     api_key: None = Security(auth.get_api_key),
# ):
#     allowed_types = ["image/jpeg", "image/jpg", "image/png"]
#     logger.info("Content Type: " + file.content_type)
#     if file.content_type not in allowed_types:
#         logger.info(msg.FILE_TYPE_NOT_ALLOWED)
#         raise HTTPException(
#             status_code=400,
#             detail=msg.FILE_TYPE_NOT_ALLOWED,
#         )
#     if not achievements.get_ach_by_key(db, achievement):
#         logger.info(msg.ACHIEVEMENT_NOT_EXISTS)
#         raise HTTPException(status_code=404, detail=msg.ACHIEVEMENT_NOT_EXISTS)
#     logger.info("File size: " + str(file.size))
#     if file.size > 512000:
#         logger.info(msg.FILE_TOO_BIG_ACHIEVEMENTS)
#         raise HTTPException(status_code=400, detail=msg.FILE_TOO_BIG)
#     try:
#         data = await file.read()
#         achievements.upload_image(db, achievement, data)
#         return "Image uploaded"
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/achievement-image/{achievement}")
# @version(1)
# async def get_achievement_image(
#     achievement: str,
#     db: Session = Depends(get_db),
#     api_key: None = Security(auth.get_api_key),
# ):
#     if not achievements.get_ach_by_key(db, achievement):
#         logger.info(msg.ACHIEVEMENT_NOT_EXISTS)
#         raise HTTPException(status_code=404, detail=msg.ACHIEVEMENT_NOT_EXISTS)
#     try:
#         data = achievements.get_image(db, achievement)
#         if data[0] is None:
#             return Response(content="Achievement has no image", status_code=400)
#         return Response(content=data[0], media_type="image/jpeg")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
