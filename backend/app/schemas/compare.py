"""
Compare Schemas
複数資産比較用スキーマ
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import date


class AssetSymbol(BaseModel):
    """資産シンボル"""
    symbol: str = Field(..., description="シンボル/銘柄コード")
    asset_type: str = Field(..., description="資産クラス (jp_stock, us_stock, crypto, fx)")
    name: Optional[str] = Field(None, description="表示名")


class CompareRequest(BaseModel):
    """比較リクエスト"""
    assets: List[AssetSymbol] = Field(..., description="比較する資産リスト", max_items=10)
    start_date: Optional[date] = Field(None, description="開始日（基準日）")
    period: Optional[str] = Field("1y", description="期間 (1mo, 3mo, 6mo, 1y, 5y)")


class DataPoint(BaseModel):
    """データポイント"""
    date: str
    value: float
    normalized_value: float  # 基準日を100とした正規化値


class AssetPerformance(BaseModel):
    """資産パフォーマンス"""
    symbol: str
    asset_type: str
    name: str
    data: List[DataPoint]
    total_return: float = Field(..., description="総リターン（%）")
    volatility: Optional[float] = Field(None, description="ボラティリティ")
    max_drawdown: Optional[float] = Field(None, description="最大ドローダウン（%）")


class CompareResponse(BaseModel):
    """比較レスポンス"""
    assets: List[AssetPerformance]
    start_date: str
    end_date: str
    ranking: List[Dict[str, Any]] = Field(..., description="パフォーマンスランキング")
