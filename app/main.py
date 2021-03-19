import os
import json

from fastapi import FastAPI

from app.libs.test_math import add_numbers
from app.routers import tools

from app.dependencies import metadata_tags

DB_DIR = os.path.join("app", "db")
DB_PATH = os.path.join(DB_DIR, "db.json")

app = FastAPI(
    title="SecuritiesAnalysisTools API",
    description="The FastAPI version of SecuritiesAnalysisTools repo.",
    version="0.0.1",
    openapi_tags=metadata_tags.tags_metadata
)

app.include_router(tools.router)


def init_db():
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)
    if not os.path.exists(DB_PATH):
        return {}

    with open(DB_PATH, 'r') as dbf:
        db = json.load(dbf)
        dbf.close()

    return db


DB = init_db()


@app.get("/")
def check_heartbeat():
    return {"hello there": "from SAT-FastAPI"}


@app.get("/{ticker}")
def echo_ticker(ticker: str):
    return {"ticker": ticker}


@app.post("/add_values/{a}/{b}")
def echo_add(a: int, b: int):
    value = add_numbers(a, b)
    return {"value": value}
