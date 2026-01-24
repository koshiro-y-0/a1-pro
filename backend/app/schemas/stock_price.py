"""
Stock Price Schemas
株価関連のPydanticスキーマ
"""

from pydantic import BaseModel
from datetime import date


class StockPriceData(BaseModel):
    """株価データスキーマ"""
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class StockPriceResponse(BaseModel):
    """株価レスポンススキーマ"""
    stock_code: str
    period: str
    data: list[StockPriceData]
