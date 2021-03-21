from fastapi import APIRouter

from app.libs.utils.classes import ToolConfig
from app.libs.utils.responses import response_handler

from app.libs.tools.rsi import generate_rsi_signal


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
