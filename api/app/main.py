from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

from .config import Config
from .database import models
from .database.database import SessionLocal, engine
from .routers import admin, basic, bot, games, statistics, users
from .utils import logger

models.Base.metadata.create_all(bind=engine)

config = Config()

app = FastAPI(title="LaViciacion API", version="0.1.0")

app.include_router(admin.router)
app.include_router(basic.router)
app.include_router(users.router)
app.include_router(games.router)
app.include_router(statistics.router)
app.include_router(bot.router)

app = VersionedFastAPI(app, version_format="{major}", prefix_format="/api/v{major}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
