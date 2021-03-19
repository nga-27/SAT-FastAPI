from typing import Optional

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
