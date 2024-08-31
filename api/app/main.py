import datetime

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

from .config import Config
from .database import models
from .database.database import SessionLocal, engine
from .routers import admin, basic, bot, games, statistics, users, utils
from .utils import logger

import sentry_sdk

config = Config()


def before_send(event, hint):
    # modify event here
    logger.debug("BEFORE SENTRY")
    logger.debug(event)
    logger.debug(hint)
    return event


sentry_sdk.init(
    dsn=config.SENTRY_URL,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    environment=config.SENTRY_ENV,
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

    # Calcula la duración de la solicitud
    duration = end_time - start_time

    # Registra la hora actual y la duración en los logs
    logger.info(
        f'REQUEST - "{request.method} {request.url.path}" - {response.status_code} - {duration}'
    )

    return response
