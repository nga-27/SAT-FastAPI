import json

from fastapi import APIRouter

from app.libs.classes import Ticker
from app.libs.data_download import download_data

router = APIRouter(
    prefix="/tools"
)


@router.get("/", tags=["tools"])
def echo_tools():
    return {"tools": "hello there"}


@router.post("/ochl", tags=["tools"])
def basic_info(ticker: Ticker):
    data = download_data(ticker)
    return {"ticker": ticker, "data": json.dumps(data)}


@router.post("/", tags=["tools"])
def store_in_db(ticker: Ticker):
    data = download_data(ticker)
    return {}
