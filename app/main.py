import os
import json
import secrets

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.dependencies import metadata_tags
from app.routers import tickers, tool
from app.users import users

from app.routers.tools import moving_average
from app.routers.tools import on_balance_volume
from app.routers.tools import oscillators
from app.routers.metadata import volatility_quotient

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
app.include_router(on_balance_volume.router)
app.include_router(oscillators.router)
app.include_router(volatility_quotient.router)


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

security = HTTPBasic()


@app.get("/", tags=["Health"])
def check_heartbeat():
    return {"hello there": "from SAT-FastAPI"}


@app.get("/auth", tags=["Health"])
def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username in USER:
        if credentials.password != "":
            correct_password = secrets.compare_digest(
                credentials.password, USER[credentials.username]['password_hash'])
            if correct_password:
                return {"status": "authorized"}
            raise HTTPException(
                status_code=401, detail=f"User '{credentials.username}' not authorized.")
        raise HTTPException(
            status_code=401, detail=f"User '{credentials.username}' not authorized.")
    raise HTTPException(
        status_code=404, detail=f"User '{credentials.username}' not found.")
