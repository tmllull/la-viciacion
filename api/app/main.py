import datetime
import sentry_sdk
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

from .config import Config
from .database import models
from .database.database import SessionLocal, engine
from .routers import admin, basic, bot, games, statistics, users, utils, webhooks
from .utils.logger import LogManager

log_manager = LogManager()
logger = log_manager.get_logger()


config = Config()


def before_send(event, hint):
    # modify event here
    logger.debug("------BEFORE SENTRY------")
    logger.debug("Event:")
    logger.debug(event)
    logger.debug("Hint:")
    logger.debug(hint)
    return event


if config.SENTRY_URL is not None and config.SENTRY_URL != "":
    sentry_sdk.init(
        dsn=config.SENTRY_URL,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
        environment=config.ENVIRONMENT,
        before_send=before_send,
    )

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LaViciacion API", version="0.1.0")

app.include_router(admin.router)
app.include_router(basic.router)
app.include_router(users.router)
app.include_router(games.router)
app.include_router(statistics.router)
app.include_router(bot.router)
app.include_router(utils.router)
app.include_router(webhooks.router)

app = VersionedFastAPI(app, version_format="{major}", prefix_format="/api/v{major}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_timestamp_to_logs(request, call_next):
    start_time = datetime.datetime.now()
    response = await call_next(request)
    end_time = datetime.datetime.now()

    duration = end_time - start_time

    query_params = request.query_params

    if query_params:
        query_str = f"?{query_params}"
    else:
        query_str = ""

    logger.info(
        f'REQUEST - "{request.method} {request.url.path}{query_str}" - {response.status_code} - {duration}'
    )

    return response
