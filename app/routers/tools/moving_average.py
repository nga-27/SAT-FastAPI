from fastapi import APIRouter

from app.libs.utils.classes import ToolConfig
from app.libs.utils.responses import response_handler

from app.libs.tools.moving_average import (
    simple_moving_avg, exponential_moving_avg, windowed_moving_avg
)


router = APIRouter(
    prefix="/tools/moving_average"
)


@router.get("/simple/{ticker}", tags=["Moving Averages"], description="default period is 7 days", status_code=200)
def get_simple_moving_average(ticker: str):
    sma = simple_moving_avg(ticker)
    response = response_handler(
        'tools', 'simple_moving_average', sma, ticker=ticker)
    return response


@router.post("/simple", tags=["Moving Averages"], status_code=201)
def post_simple_moving_average(config: ToolConfig):
    sma = simple_moving_avg(config.ticker, period=config.period)
    response = response_handler(
        'tools', 'simple_moving_average', sma, ticker=config.ticker)
    return response


@router.get("/exponential/{ticker}", tags=["Moving Averages"], description="default period is 7 days", status_code=200)
def get_exponential_moving_average(ticker: str):
    ema = exponential_moving_avg(ticker)
    response = response_handler(
        'tools', 'exponential_moving_average', ema, ticker=ticker)
    return response


@router.post("/exponential", tags=["Moving Averages"], status_code=201)
def post_exponential_moving_average(config: ToolConfig):
    ema = exponential_moving_avg(config.ticker, period=config.period)
    response = response_handler(
        'tools', 'exponential_moving_average', ema, ticker=config.ticker)
    return response


@router.get("/windowed/{ticker}",
            tags=["Moving Averages"],
            description="default period is 7 days",
            status_code=200)
def get_windowed_moving_avg(ticker: str):
    wma = windowed_moving_avg(ticker)
    response = response_handler(
        'tools', 'windowed_moving_average', wma, ticker=ticker)
    return response


@router.post("/windowed", tags=["Moving Averages"], status_code=201)
def post_windowed_moving_avg(config: ToolConfig):
    wma = windowed_moving_avg(config.ticker, period=config.period,
                              weight_strength=config.weight, subFilter=config.subFilter)
    response = response_handler(
        'tools', 'windowed_moving_average', wma, ticker=config.ticker)
    return response
