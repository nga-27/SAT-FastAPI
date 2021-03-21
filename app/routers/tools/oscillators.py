from fastapi import APIRouter

from app.libs.utils.classes import ToolConfig
from app.libs.utils.responses import response_handler

from app.libs.tools.ultimate_oscillator import ultimate_oscillator

router = APIRouter(
    prefix="/tools/oscillator"
)


@router.get("/ultimate/{ticker}", tags=["Oscillators"], status_code=200)
def get_on_balance_volume(ticker: str):
    ult = ultimate_oscillator(ticker)
    response = response_handler(
        'tools', 'ultimate_oscillator', ult, ticker=ticker)
    return response
