from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.libs.utils.classes import OscillatorConfig, ToolConfig
from app.libs.utils.responses import response_handler
from app.libs.utils.user_utils import serialize_user_secret_key

from app.libs.meta.volatility_quotient import get_volatility

security = HTTPBasic()

router = APIRouter(
    prefix="/metadata/volatility"
)


@router.get("/{ticker}", tags=["Metadata"], status_code=200)
def get_volatility_quotient(ticker: str, credentials: HTTPBasicCredentials = Depends(security)):
    vq_key, code = serialize_user_secret_key(
        credentials.username, credentials.password, 'vq_key')
    if code != 200:
        raise HTTPException(status_code=code, detail=vq_key)
    if vq_key == "":
        raise HTTPException(
            status_code=404, detail="'vq_key' not found for user.")
    vq_data = get_volatility(ticker, vq_key)
    response = response_handler(
        'metadata', 'volatility', vq_data, ticker=ticker)
    return response
