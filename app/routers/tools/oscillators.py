from fastapi import APIRouter

from app.libs.utils.classes import OscillatorConfig, ToolConfig
from app.libs.utils.responses import response_handler

from app.libs.tools.ultimate_oscillator import ultimate_oscillator
from app.libs.tools.rsi import RSI
from app.libs.tools.macd import mov_avg_convergence_divergence

router = APIRouter(
    prefix="/tools/oscillator"
)


@router.get("/ultimate/{ticker}", tags=["Oscillators"], status_code=200)
def get_ultimate_oscillator(ticker: str):
    ult = ultimate_oscillator(ticker)
    response = response_handler(
        'tools', 'ultimate_oscillator', ult, ticker=ticker)
    return response


@router.post("/ultimate", tags=["Oscillators"], status_code=201)
def post_ultimate_oscillator(config: OscillatorConfig):
    ult = ultimate_oscillator(config.ticker, config=config.period_list)
    response = response_handler(
        'tools', 'ultimate_oscillator', ult, ticker=config.ticker)
    return response


@router.get("/rsi/{ticker}", tags=["Oscillators"], status_code=200)
def get_rsi(ticker: str):
    rsi = RSI(ticker)
    response = response_handler('tools', 'rsi', rsi, ticker=ticker)
    return response


@router.post("/rsi", tags=["Oscillators"], status_code=201)
def post_rsi(config: ToolConfig):
    rsi = RSI(config.ticker, period=config.period)
    response = response_handler('tools', 'rsi', rsi, ticker=config.ticker)
    return response


@router.get("/macd/{ticker}", tags=["Oscillators"], status_code=200)
def get_macd(ticker: str):
    macd = mov_avg_convergence_divergence(ticker)
    response = response_handler('tools', 'macd', macd, ticker=ticker)
    return response
