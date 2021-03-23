from fastapi import APIRouter

from app.libs.utils.classes import OscillatorConfig, ToolConfig
from app.libs.utils.responses import response_handler

router = APIRouter(
    prefix="/metadata/volatility"
)
