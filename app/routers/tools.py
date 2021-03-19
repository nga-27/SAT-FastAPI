from fastapi import APIRouter

from app.libs.utils.classes import ToolConfig
from app.libs.utils.responses import response_handler

from app.libs.tools.rsi import generate_rsi_signal
from app.libs.tools.moving_average import (
    simple_moving_avg, exponential_moving_avg, windowed_moving_avg
)


LIST_OF_TOOLS = [
    "rsi",
    "simple_moving_average",
    "exponential_moving_average",
    "windowed_moving_average"
]

router = APIRouter(
    prefix="/tools"
)


@router.get("/", tags=["Tools"])
def echo_tools():
    return {"tools available": LIST_OF_TOOLS}


@router.get("/rsi/{ticker}", tags=["RSI"], status_code=200)
def get_rsi(ticker: str):
    rsi = generate_rsi_signal(ticker)
    response = response_handler('tools', 'rsi', rsi, ticker=ticker)
    return response


@router.post("/rsi", tags=["RSI"], status_code=201)
def post_rsi(config: ToolConfig):
    rsi = generate_rsi_signal(config.ticker, period=config.period)
    response = response_handler('tools', 'rsi', rsi, ticker=config.ticker)
    return response


@router.get("/simple_moving_average/{ticker}", tags=["Moving Averages"], description="default period is 7 days", status_code=200)
def get_simple_moving_average(ticker: str):
    sma = simple_moving_avg(ticker)
    response = response_handler(
        'tools', 'simple_moving_average', sma, ticker=ticker)
    return response


@router.post("/simple_moving_average", tags=["Moving Averages"], status_code=201)
def post_simple_moving_average(config: ToolConfig):
    sma = simple_moving_avg(config.ticker, period=config.period)
    response = response_handler(
        'tools', 'simple_moving_average', sma, ticker=config.ticker)
    return response


@router.get("/exponential_moving_average/{ticker}", tags=["Moving Averages"], description="default period is 7 days", status_code=200)
def get_simple_moving_average(ticker: str):
    ema = exponential_moving_avg(ticker)
    response = response_handler(
        'tools', 'exponential_moving_average', ema, ticker=ticker)
    return response


@router.post("/exponential_moving_average", tags=["Moving Averages"], status_code=201)
def post_simple_moving_average(config: ToolConfig):
    ema = exponential_moving_avg(config.ticker, period=config.period)
    response = response_handler(
        'tools', 'exponential_moving_average', ema, ticker=config.ticker)
    return response


@router.get("/windowed_moving_average/{ticker}", tags=["Moving Averages"], description="default period is 7 days", status_code=200)
def get_windowed_moving_avg(ticker: str):
    wma = windowed_moving_avg(ticker)
    response = response_handler(
        'tools', 'windowed_moving_average', wma, ticker=ticker)
    return response


@router.post("/windowed_moving_average", tags=["Moving Averages"], status_code=201)
def post_windowed_moving_avg(config: ToolConfig):
    wma = windowed_moving_avg(config.ticker, period=config.period,
                              weight_strength=config.weight, subFilter=config.subFilter)
    response = response_handler(
        'tools', 'windowed_moving_average', wma, ticker=config.ticker)
    return response
