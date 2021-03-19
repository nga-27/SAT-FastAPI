from typing import Optional

from pydantic import BaseModel


class Ticker(BaseModel):
    ticker: str
    period: Optional[str] = '2y'
    interval: Optional[str] = '1d'
