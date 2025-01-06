from fastapi import Depends
from strawberry.fastapi import GraphQLRouter
from ..database.graphql.schemas import schema

from .. import auth
from ..database import models
from ..database.database import engine
from ..utils import actions as actions
from ..utils.logger import LogManager

log_manager = LogManager()
logger = log_manager.get_logger()

graphql_app = GraphQLRouter(
    prefix="/graphql",
    schema=schema,
    tags=["GraphQL"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(auth.check_api_or_token_auth)],
)

models.Base.metadata.create_all(bind=engine)

# router = APIRouter(
#     # prefix="/graphql",
#     tags=["GraphQL"],
#     responses={404: {"description": "Not found"}},
#     dependencies=[Depends(auth.check_api_or_token_auth)],
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
