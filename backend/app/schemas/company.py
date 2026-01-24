"""
Company Schemas
企業関連のPydanticスキーマ
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CompanyBase(BaseModel):
    """企業の基本情報"""
    stock_code: str
    name: str
    industry: Optional[str] = None
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    """企業作成用スキーマ"""
    pass


class CompanyUpdate(BaseModel):
    """企業更新用スキーマ"""
    name: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None


class CompanyResponse(CompanyBase):
    """企業レスポンススキーマ"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CompanySearchResult(BaseModel):
    """検索結果スキーマ"""
    id: int
    stock_code: str
    name: str
    industry: Optional[str] = None

    class Config:
        from_attributes = True
