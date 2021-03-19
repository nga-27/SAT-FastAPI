import json

from fastapi import APIRouter

from app.libs.utils.classes import Ticker
from app.libs.utils.db_utils import download_data

router = APIRouter(
    prefix="/tickers"
)


@router.get("/{ticker}", tags=["Basic Ticker"])
def echo_ticker(ticker: str):
    return {"ticker": ticker.upper()}


@router.post("/ochl", tags=["Basic Ticker"])
def basic_info(ticker: Ticker):
    data = download_data(ticker)
    return {"ticker": ticker, "data": json.dumps(data)}


@router.post("/", tags=["Basic Ticker"], description="Store a ticker in the DB")
def store_in_db(ticker: Ticker):
    data = download_data(ticker)
    return {"status": "success", "ticker": ticker}
