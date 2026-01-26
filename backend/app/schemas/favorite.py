"""
Favorite Schemas
お気に入り関連のPydanticスキーマ
"""

from pydantic import BaseModel
from datetime import datetime


class FavoriteCreate(BaseModel):
    """お気に入り作成用スキーマ"""
    company_id: int


class FavoriteResponse(BaseModel):
    """お気に入りレスポンススキーマ"""
    id: int
    company_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FavoriteWithCompany(FavoriteResponse):
    """企業情報付きお気に入り"""
    stock_code: str
    company_name: str
    industry: str | None = None
