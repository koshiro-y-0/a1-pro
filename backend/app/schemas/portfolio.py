"""
Portfolio Schemas
ポートフォリオ関連のPydanticスキーマ
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class PortfolioBase(BaseModel):
    """ポートフォリオの基本情報"""
    asset_type: str = Field(..., description="資産クラス (jp_stock, us_stock, crypto, fx)")
    symbol: str = Field(..., description="銘柄コード/シンボル")
    purchase_date: date = Field(..., description="購入日")
    purchase_price: float = Field(..., gt=0, description="購入価格")
    quantity: float = Field(..., gt=0, description="数量")


class PortfolioCreate(PortfolioBase):
    """ポートフォリオ作成用スキーマ"""
    pass


class PortfolioUpdate(BaseModel):
    """ポートフォリオ更新用スキーマ"""
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = Field(None, gt=0)
    quantity: Optional[float] = Field(None, gt=0)


class PortfolioResponse(PortfolioBase):
    """ポートフォリオレスポンススキーマ"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PortfolioWithPerformance(PortfolioResponse):
    """パフォーマンス情報付きポートフォリオ"""
    current_price: Optional[float] = None
    current_value: Optional[float] = None
    profit_loss: Optional[float] = None
    profit_loss_percentage: Optional[float] = None
    company_name: Optional[str] = None
