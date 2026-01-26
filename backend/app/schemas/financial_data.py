"""
Financial Data Schemas
決算データ関連のPydanticスキーマ
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FinancialDataBase(BaseModel):
    """決算データの基本情報"""
    company_id: int
    fiscal_year: int
    fiscal_quarter: Optional[int] = None
    revenue: Optional[int] = None
    operating_profit: Optional[int] = None
    ordinary_profit: Optional[int] = None
    net_profit: Optional[int] = None
    total_assets: Optional[int] = None
    equity: Optional[int] = None
    total_liabilities: Optional[int] = None
    current_assets: Optional[int] = None
    current_liabilities: Optional[int] = None


class FinancialDataCreate(FinancialDataBase):
    """決算データ作成用スキーマ"""
    pass


class FinancialDataResponse(FinancialDataBase):
    """決算データレスポンススキーマ"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FinancialMetrics(BaseModel):
    """財務指標スキーマ"""
    equity_ratio: Optional[float] = None  # 自己資本比率
    current_ratio: Optional[float] = None  # 流動比率
    debt_ratio: Optional[float] = None  # 負債比率
    roe: Optional[float] = None  # ROE
    operating_margin: Optional[float] = None  # 営業利益率


class FinancialDataWithMetrics(FinancialDataResponse):
    """財務指標付き決算データ"""
    metrics: FinancialMetrics


class CombinedDataResponse(BaseModel):
    """複合データレスポンススキーマ"""
    fiscal_year: int
    revenue: Optional[int] = None
    ordinary_profit: Optional[int] = None
    stock_price: Optional[float] = None
