from typing import Optional
import uuid

from pydantic import BaseModel


class Ticker(BaseModel):
    ticker: str
    period: Optional[str] = '2y'
    interval: Optional[str] = '1d'


class ToolConfig(BaseModel):
    ticker: str
    period: Optional[int] = None
    weight: Optional[float] = 2.0
    subFilter: Optional[str] = "simple"


class OscillatorConfig(BaseModel):
    ticker: str
    period_list: Optional[list] = [7, 14, 28]


class User(BaseModel):
    username: str
    name: Optional[str] = ""
    uuid: Optional[str] = str(uuid.uuid4())
    password_hash: Optional[str] = ""
    vq_key: Optional[str] = ""
