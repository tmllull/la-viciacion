from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Security, status
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
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
@version(1)
def hello_world(request: Request):
    """
    Test endpoint
    """
    # return {"message": "Hello World", "root_path": request.scope.get("root_path")}
    return "API is working!"


@router.post("/login")
@version(1)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    Login endpoint
    """
    return await login_for_access_token(form_data, db)


@router.post("/signup")
@version(1)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.invitation_key != config.INVITATION_KEY:
        raise HTTPException(status_code=400, detail="Invalid invitation key")
    db_user = users.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return users.create_user(db=db, user=user)


@router.post("/token", response_model=auth.Token)
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
        data={
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "telegram_id": user.telegram_id,
            "clockify_id": user.clockify_id,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
        },
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/active_user", response_model=schemas.User)
@version(1)
def active_user(user: models.User = Security(auth.get_current_active_user)):
    """
    Get active user info
    """
    return user
