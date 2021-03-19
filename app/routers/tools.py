from fastapi import APIRouter

from app.libs.tools.rsi import generate_rsi_signal
from app.libs.utils.responses import response_handler


LIST_OF_TOOLS = [
    "RSI"
]

router = APIRouter(
    prefix="/tools"
)


@router.get("/", tags=["Tools"])
def echo_tools():
    return {"tools available": LIST_OF_TOOLS}


@router.get("/rsi/{ticker}", tags=["Tools"])
def get_rsi(ticker: str):
    rsi = generate_rsi_signal(ticker)
    response = response_handler('tools', 'rsi', rsi, ticker=ticker)
    return response
