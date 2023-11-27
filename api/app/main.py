from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

from .config import Config
from .database import models
from .database.database import engine
from .routers import basic, games, statistics, users

models.Base.metadata.create_all(bind=engine)

config = Config()

app = FastAPI(
    title="LaViciacion API",
    version="0.1.0",
)

app.include_router(basic.router)
app.include_router(users.router)
app.include_router(games.router)
app.include_router(statistics.router)

app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
