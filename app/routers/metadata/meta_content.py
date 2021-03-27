from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.libs.utils.classes import OscillatorConfig, ToolConfig
from app.libs.utils.responses import response_handler
from app.libs.utils.user_utils import serialize_user_secret_key

security = HTTPBasic()

router = APIRouter(
    prefix="/metadata/"
)
