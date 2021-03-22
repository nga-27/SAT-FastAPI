from fastapi import APIRouter

from app.libs.utils.responses import response_handler

from app.libs.tools.on_balance_volume import generate_obv_signal

router = APIRouter(
    prefix="/tools/on_balance_vol"
)


@router.get("/{ticker}", tags=["On Balance Volume"], status_code=200)
def get_on_balance_volume(ticker: str):
    obv = generate_obv_signal(ticker)
    response = response_handler(
        'tools', 'on_balance_volume', obv, ticker=ticker)
    return response
