from enum import Enum
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_versioning import version
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter
from ..database.graphql.schemas import schema

from .. import auth
from ..database.crud import users as users_crud
from ..database import models, schemas
from ..database.database import SessionLocal, engine
from ..routers import admin, games, statistics, users, utils
from ..utils import actions as actions
from ..utils.logger import LogManager

log_manager = LogManager()
logger = log_manager.get_logger()

graphql_app = GraphQLRouter(
    prefix="/graphql",
    schema=schema,
    tags=["GraphQL"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(auth.check_any_auth)],
)

models.Base.metadata.create_all(bind=engine)

# router = APIRouter(
#     # prefix="/graphql",
#     tags=["GraphQL"],
#     responses={404: {"description": "Not found"}},
#     dependencies=[Depends(auth.get_api_key)],
# )


# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @graphql_app.get("/")
# # @version(1)
# def get_user(db: Session = Depends(get_db)):
#     return users.get_users()
