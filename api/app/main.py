from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI

from .routers import basic, games, statistics, users

app = FastAPI()

app.include_router(basic.router)
app.include_router(users.router)
app.include_router(games.router)
app.include_router(statistics.router)

app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}")
