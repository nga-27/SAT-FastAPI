import os
import json

from fastapi import FastAPI

from app.routers import tickers, tool
from app.routers.tools import moving_average
from app.users import users
from app.dependencies import metadata_tags

DB_DIR = os.path.join("app", "db")
DB_PATH = os.path.join(DB_DIR, "db.json")
USER_PATH = os.path.join(DB_DIR, "user.json")

app = FastAPI(
    title="SecuritiesAnalysisTools API",
    description="The FastAPI version of SecuritiesAnalysisTools repo.",
    version="0.0.2",
    openapi_tags=metadata_tags.tags_metadata
)

app.include_router(tickers.router)
app.include_router(tool.router)
app.include_router(users.router)
app.include_router(moving_average.router)


def init_db():
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)
    if not os.path.exists(DB_PATH):
        return {}

    with open(DB_PATH, 'r') as dbf:
        db = json.load(dbf)
        dbf.close()

    return db


def init_user():
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)
    if not os.path.exists(USER_PATH):
        return {}

    with open(USER_PATH, 'r') as usf:
        user = json.load(usf)
        usf.close()

    return user


DB = init_db()
USER = init_user()


@app.get("/", tags=["Health"])
def check_heartbeat():
    return {"hello there": "from SAT-FastAPI"}
